from dataclasses import dataclass
from typing import Dict, Optional
from analyzers import VideoAnalysisResult, AudioAnalysisResult, TextAnalysisResult


@dataclass
class CombinedScore:
    overall: float
    breakdown: Dict[str, float]
    summary: str


def compute_combined_score(
    video: Optional[VideoAnalysisResult],
    audio: Optional[AudioAnalysisResult],
    text: Optional[TextAnalysisResult],
) -> CombinedScore:
    subscores: Dict[str, float] = {}

    if video is not None:
        emotion_pos = video.emotion_scores.get("happy", 0.0) + video.emotion_scores.get("neutral", 0.0) * 0.5
        headpose_stability = 1.0 - min(1.0, (abs(video.head_pose.get("yaw", 0.0)) + abs(video.head_pose.get("pitch", 0.0))) / 2.0)
        subscores["visual"] = max(0.0, min(1.0, 0.4 * emotion_pos + 0.4 * video.gaze_engagement + 0.2 * headpose_stability))
    if audio is not None:
        pitch_score = 1.0 - min(1.0, abs(audio.voice_pitch_hz - 180.0) / 180.0)
        rate_score = 1.0 - min(1.0, abs(audio.speech_rate_wpm - 140.0) / 140.0)
        speaking = audio.speaking_ratio
        subscores["audio"] = max(0.0, min(1.0, 0.34 * pitch_score + 0.33 * rate_score + 0.33 * speaking))
    if text is not None:
        disc_balance = 1.0 - min(1.0, max(text.disc_scores.values()) - min(text.disc_scores.values()))
        intrinsic = sum(text.intrinsic_traits.values()) / max(1, len(text.intrinsic_traits))
        subscores["textual"] = max(0.0, min(1.0, 0.4 * text.sentiment + 0.3 * text.clarity + 0.3 * (0.5 * disc_balance + 0.5 * intrinsic)))

    if subscores:
        overall = sum(subscores.values()) / len(subscores)
    else:
        overall = 0.5

    summary = (
        f"Overall: {overall:.2f}. "
        f"Visual: {subscores.get('visual', 0.0):.2f}, "
        f"Audio: {subscores.get('audio', 0.0):.2f}, "
        f"Textual: {subscores.get('textual', 0.0):.2f}."
    )

    return CombinedScore(overall=overall, breakdown=subscores, summary=summary)








































