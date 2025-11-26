import requests
import json
import os
import time
from openai import OpenAI

client = OpenAI(
    api_key="xxx"
)

ThomAIs_on = False
guest = True

def create_input(query, memory0=None, definitions="", data=""):
    input = [
        {"role": "user", "content": "I am a researcher and need accurate and considerate responses."},
        {"role": "assistant", "content": "I will provide accurate amd nuanced responses, focused on being based on clear evidence and referring to any relevant theories or data."},
    ]
    if ThomAIs_on:
        input.append({"role": "user",
                                    "content": "Be aware of the following ideas, findings, references, and arguments; use their style of speaking and argumentation: " + fThomasAIs()})
        input.append({"role": "assistant",
                                "content": "I will use these ideas where relevant, and will follow the style of thinking and argumentation."})
    if len(data) > 0:
        input.append({"role": "user", "content": "Use the following information where relevant when answering questions: " + data})
        input.append({"role": "assistant", "content": "I will check whether this information is relevant and use it if so."})
    if not memory0 is None:
        for mem0 in memory0:
            if len(mem0["content"]) > 0 and not mem0 is None:
                input.append(mem0)
    if len(definitions) > 0:
        input.append({"role": "user", "content": "Use the following definitions of terms: " + definitions})
        input.append({"role": "assistant", "content": "I will make sure to apply these definitions in any relevant responses."})
    input.append({"role": "user", "content": query})
    return input

def query_AI_chat(input):
    response = client.chat.completions.create(
        model="gpt-5",
        messages=input,
        max_completion_tokens=1000
    )
    return response.choices[0].message

def query_AI(input):
    response = client.responses.create(
        model="gpt-5",
        input=input
    )
    return response.output_text

def fThomasAIs():
    BeliefsAndOpinionsStr = ''
    BeliefsAndOpinionsStr = BeliefsAndOpinionsStr + """
   - Predictive Visual Probe Task (cVPT): Uses predictive cues to indicate where emotionally salient (but task-irrelevant) stimuli may appear; probe-only trials yield an anticipatory attentional bias indexed by RTs to predicted locations. This design reduces exemplar-driven noise and can produce reliable bias scores (typically ~.7–.8; up to .89 with blockwise probe-location probabilities). Biases relate to risky drinking and anxiety, and reliability collapses when cues are nonpredictive, supporting a genuinely anticipatory component. Independent replications report good reliability and anxiety links.
- Trial-to-trial carryover: Attentional bias on trial N depends on the previous probe’s location (N−1), including asymmetric effects for threat. Robust in a “diagonalized” VPT with direct location–response mapping; largely absent in standard dot-probe tasks.
- Threat anticipation and freezing: Freezing (reduced sway/bradycardia) reflects action preparation: being armed increases freezing; threat slows responses on unrelated tasks starting ~600 ms post-cue and diminishing by ~1200 ms. Threat can also lower thresholds for threat-relevant actions (apparent impulsivity). Sleep deprivation mainly reduces accuracy.
- R3 “Reflective Cycle” model: Recasts impulsive–reflective differences as a continuous response-selection delay parameter shaped by learning; simulations illustrate threshold dynamics. Large language models can serve as proxies for “automatic associations” (semantic similarity predicts IAT effects) and may aid stimulus selection.
- ABM control issue: The common “random” control likely trains irrelevance (an active intervention), while active ABM can inadvertently increase salience (“salience side-effect”). Predictive-cue ABM may avoid this by training toward/away from predicted categories rather than presented exemplars; initial evidence supports feasibility.
Overall: With predictive cues and optimized designs, behavioral measures of attentional bias can be reliable and informative.
- Thesis: “No” to all five prompts: traditional theism need not imply biblical literalism/creationism; science and (well-defined) religion need not conflict; God-of-the-gaps is not required; the Problem of Evil isn’t decisively atheistic; eternal life isn’t “hell for wrong dogma.”
- Core case: Across two millennia, major Jewish and Christian thinkers (e.g., Origen, Augustine, Maimonides, Calvin, Galileo, Temple, Lewis, modern scholars) reject literalist readings of Genesis and anthropomorphic views of God, stressing that Scripture teaches salvation, not science, and often speaks figuratively.
- Science–faith: Evolution and natural law can be understood as expressions of divine providence; literalism is a modern aberration, not historic orthodoxy. Both anti-religious polemics and creationist readings commit category errors by treating theological texts as scientific treatises.
- Conclusion: “Old-school” theism is compatible with non-literal interpretation and scientific inquiry; equating theism with creationism or anti-science is a strawman.
- Core question: What, if anything, grounds or transcends the empirically observable universe? Scientific progress intensifies, not removes, this question.
- Science: a falsification-based method limited to intersubjective, testable claims; it is neutral on unfalsifiable metaphysics. Qualia exemplify intrinsic limits.
- Reductionism points toward an ultimate, elegant principle—conceptually close to a non-anthropomorphic, transcendent God.
- Distinguish religions: tribal-dogmatic (often anti-scientific) vs experiential-transformative (science-compatible, focused on lived transformation).
- Religious reasoning as iterative model-building: subjective experience plus rational constraints and coherence tests; revelation is critically evaluated.
- Implicit God-definition: the transcendent ground of lawfulness and consciousness and the loving Presence in religious experience—one parsimonious source of both.
- Objections addressed: God needn’t be complex; first-cause requires transcendence; evil as “necessary” for life/agency (“multiversal mercy” reframes suffering).
- Eschatology reimagined: “eternal life” as convergence to stable, altruistic consciousness; judgment centers on enacted love (Mt 25). Conclusion: non-fundamentalist theism can complement science; “God is love.”
- Student cheating (e.g., contract cheating ~15%) matters, but research misconduct also harms students.
- Three harms: degrades the literature and culture (hype, replication crisis); models unethical norms students observe (bullying, p-hacking, credit theft); directly exposes future researchers to exploitation.
- Introduces “Questionable Collaboration Practices” (QCP): exploitation in collaborations that violate consent, contribution, and credit (pressure to work, disproportionate benefit, misattributed authorship/supervisor exploitation).
- Good collaboration = necessary, real contributions with fair credit; train students to identify “real” contributions and beware token/middle‑man roles or mere access-trading for authorship.
- Teaching via Theory of Planned Behaviour: set clear norms (codes, curricula), boost control (role‑play, documentation, written agreements, ghost authorship awareness), shape attitudes (ethics and self‑interest).
- Practical advice: vet supervisors/labs, talk to current/previous students, check trainee outputs, keep records, agree contributions early in writing.
- Conclusion: Make QCP education explicit alongside p‑hacking/bullying/harassment; leadership must discourage exploitative incentives. Education can’t fix the system alone but is essential for prevention and student wellbeing.
    """
    return BeliefsAndOpinionsStr
