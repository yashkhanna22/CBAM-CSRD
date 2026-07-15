import json

from engine.models import (
    AssessmentOutput,
    CBAMAssessment,
    CSRDAssessment,
)


class OutputParser:
    """
    Converts the LLM JSON response into AssessmentOutput.
    """

    @staticmethod
    def _ensure_bool(value, default=False):
        return value if isinstance(value, bool) else default

    @staticmethod
    def _ensure_float(value, default=0.0):
        try:
            value = float(value)
            if 0.0 <= value <= 1.0:
                return value
        except (TypeError, ValueError):
            pass
        return default

    @staticmethod
    def _ensure_list(value):
        return value if isinstance(value, list) else []

    @staticmethod
    def _ensure_str(value, default=""):
        return value if isinstance(value, str) else default

    def parse(self, response: str) -> AssessmentOutput:

        try:
            data = json.loads(response)

        except json.JSONDecodeError as e:
            raise ValueError(
                f"Invalid JSON returned by LLM:\n\n{response}"
            ) from e

        cbam = data.get("cbam", {})
        csrd = data.get("csrd", {})

        return AssessmentOutput(

            cbam=CBAMAssessment(

                applicable=self._ensure_bool(
                    cbam.get("applicable")
                ),

                confidence=self._ensure_float(
                    cbam.get("confidence")
                ),

                reasoning=self._ensure_str(
                    cbam.get("reasoning")
                ),

                articles=self._ensure_list(
                    cbam.get("articles")
                ),

                assumptions=self._ensure_list(
                    cbam.get("assumptions")
                ),

                recommendations=self._ensure_list(
                    cbam.get("recommendations")
                ),

                missing_information=self._ensure_list(
                    cbam.get("missing_information")
                )

            ),

            csrd=CSRDAssessment(

                applicable=self._ensure_bool(
                    csrd.get("applicable")
                ),

                confidence=self._ensure_float(
                    csrd.get("confidence")
                ),

                reasoning=self._ensure_str(
                    csrd.get("reasoning")
                ),

                articles=self._ensure_list(
                    csrd.get("articles")
                ),

                assumptions=self._ensure_list(
                    csrd.get("assumptions")
                ),

                recommendations=self._ensure_list(
                    csrd.get("recommendations")
                ),

                missing_information=self._ensure_list(
                    csrd.get("missing_information")
                )

            ),

            executive_summary=self._ensure_str(
                data.get("executive_summary")
            ),

            consultant_notes=self._ensure_str(
                data.get("consultant_notes")
            ),

            risk_rating=self._ensure_str(
                data.get("risk_rating"),
                "Unknown"
            )

        )