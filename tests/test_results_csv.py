import csv
import io
import unittest
from pathlib import Path

from src.results_csv import (
    PromptRegressionCase,
    ResultsCSVError,
    read_prompt_regression_csv,
    read_results_csv,
    summarize,
    summarize_prompt_regression,
)


HEADER = ["model", "input", "expected", "response", "correct"]


def make_csv(extra_columns, records):
    out = io.StringIO(newline="")
    writer = csv.writer(out)
    writer.writerow([*HEADER, *extra_columns])
    writer.writerows(records)
    return out.getvalue().encode("utf-8-sig")


class ResultsCSVTests(unittest.TestCase):
    def make_regression_csv(self, rows):
        out = io.StringIO(newline="")
        writer = csv.writer(out)
        writer.writerow([
            "input", "expected", "original_response", "original_correct",
            "degraded_response", "degraded_correct",
        ])
        writer.writerows(rows)
        return out.getvalue().encode("utf-8-sig")

    def test_prompt_regression_drop_tie_and_improvement(self):
        cases_drop = [
            PromptRegressionCase(1, "A", "Rede", "Rede", True, "Hardware", False),
            PromptRegressionCase(2, "B", "Rede", "Rede", True, "Rede", False),
        ]
        cases_tie = [
            PromptRegressionCase(1, "A", "Rede", "Rede", True, "Rede", True),
            PromptRegressionCase(2, "B", "Hardware", "Hardware", True, "Rede", True),
        ]
        cases_improve = [
            PromptRegressionCase(1, "A", "Rede", "Acesso", False, "Rede", True),
            PromptRegressionCase(2, "B", "Hardware", "Rede", False, "Hardware", True),
        ]

        drop = summarize_prompt_regression(cases_drop)
        tie = summarize_prompt_regression(cases_tie)
        improve = summarize_prompt_regression(cases_improve)
        self.assertEqual(drop["status"], "queda")
        self.assertEqual(drop["difference_points"], -100)
        self.assertEqual(tie["status"], "estabilidade")
        self.assertEqual(tie["difference_points"], 0)
        self.assertEqual(improve["status"], "melhora")
        self.assertEqual(improve["difference_points"], 100)

    def test_prompt_regression_published_values(self):
        content = Path(
            "eval/results/results_old/regression_results_prompt_comparison.csv"
        ).read_bytes()
        stats = summarize_prompt_regression(read_prompt_regression_csv(content))
        self.assertEqual(stats["count"], 20)
        self.assertEqual(stats["original_correct"], 10)
        self.assertEqual(stats["degraded_correct"], 3)
        self.assertAlmostEqual(stats["original_accuracy"], 0.50)
        self.assertAlmostEqual(stats["degraded_accuracy"], 0.15)
        self.assertAlmostEqual(stats["difference_points"], -35)

    def test_prompt_regression_rejects_invalid_input(self):
        invalid_contents = [
            b"input,expected\nA,Rede\n",
            b"",
            self.make_regression_csv([
                ["A", "Rede", "Rede", "talvez", "Hardware", "false"],
            ]),
            self.make_regression_csv([
                ["", "Rede", "Rede", "true", "Hardware", "false"],
            ]),
        ]
        for content in invalid_contents:
            with self.subTest(content=content):
                with self.assertRaises(ResultsCSVError):
                    read_prompt_regression_csv(content)
    def test_false_and_blank_response_stay_in_accuracy_denominator(self):
        content = make_csv(["judge_correct", "judge_reason"], [
            ["modelo", "Acesso, por favor", "Acesso", "Acesso.", "True", "true", "ok"],
            ["modelo", "Sem resposta", "Rede", "", "False", "", ""],
            ["modelo", "Sem sinal", "Rede", "Acesso", "false", "true", "Juiz discordou"],
        ])
        cases = read_results_csv(content)[None]["modelo"]
        self.assertAlmostEqual(summarize(cases)["accuracy"], 1 / 3)
        self.assertEqual(cases[0].ticket, "Acesso, por favor")
        self.assertEqual(cases[0].response, "Acesso.")
        self.assertIsNone(cases[1].judge_correct)
        self.assertFalse(cases[2].correct)
        self.assertTrue(cases[2].judge_correct)

    def test_versions_and_models_are_not_pooled(self):
        content = make_csv(["prompt_version"], [
            ["m1", "A", "Rede", "Rede", "true", "v1"],
            ["m1", "A", "Rede", "Acesso", "false", "v2"],
            ["m2", "A", "Rede", "Rede", "true", "v1"],
            ["m2", "B", "Rede", "Rede", "true", ""],
        ])
        groups = read_results_csv(content)
        self.assertEqual(set(groups), {"v1", "v2", None})
        self.assertEqual(set(groups["v1"]), {"m1", "m2"})
        self.assertEqual(summarize(groups["v2"]["m1"])["correct"], 0)
        self.assertEqual(summarize(groups["v1"]["m1"])["count"], 1)
        self.assertEqual(groups[None]["m2"][0].record, 4)

    def test_totals_distinguish_zero_from_missing_measurements(self):
        content = make_csv(["latency_seconds", "total_tokens"], [
            ["m", "A", "Rede", "Rede", "true", 0, 0],
            ["m", "B", "Rede", "Rede", "true", "0.25", 8],
            ["m", "C", "Rede", "Rede", "true", "", ""],
        ])
        cases = read_results_csv(content)[None]["m"]
        self.assertEqual(summarize(cases[:1])["total_tokens"], 0)
        self.assertEqual(summarize(cases[:2])["latency_seconds"], 0.25)
        self.assertEqual(summarize(cases[:2])["total_tokens"], 8)
        self.assertIsNone(summarize(cases)["latency_seconds"])
        self.assertIsNone(summarize(cases)["total_tokens"])

    def test_rejects_malformed_csv_instead_of_silently_skipping_rows(self):
        header = ",".join(HEADER)
        for value in [
            "model,input,expected\nm,A,Rede\n", header + "\n",
            header + '\nm,"sem fechar,Rede,Acesso,false',
            header + "\nm,A,Rede,Rede,true,extra", header + "\nm,A,Rede",
            header + ",correct\nm,A,Rede,Rede,true,false", b"\xff\xfeBAD",
        ]:
            with self.subTest(value=value), self.assertRaises(ResultsCSVError):
                read_results_csv(value)

    def test_rejects_invalid_verdicts_and_measurements(self):
        for extra, row in [
            ([], ["m", "A", "Rede", "", "true"]),
            ([], ["m", "A", "Rede", "Rede", "talvez"]),
            (["judge_correct"], ["m", "A", "Rede", "Rede", "true", "sim"]),
            (["latency_seconds"], ["m", "A", "Rede", "Rede", "true", "NaN"]),
            (["total_tokens"], ["m", "A", "Rede", "Rede", "true", "-1"]),
        ]:
            with self.subTest(row=row), self.assertRaisesRegex(ResultsCSVError, "Linha 2"):
                read_results_csv(make_csv(extra, [row]))
