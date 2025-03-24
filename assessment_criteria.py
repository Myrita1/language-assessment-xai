def create_ilr_prompt(question, learner_response):
    return f"""
You are an expert language proficiency assessor using the official May 2021 ILR Speaking Proficiency guidelines.

TASK: Assess the learner’s response according to the following ILR criteria levels (0 through 5), across these four aspects:

1. **Functional Ability (green)**: What communicative acts or tasks can the learner perform?
2. **Precision of Forms and Meanings (red)**: How accurate, complex, and nuanced are their forms and meanings?
3. **Content Meaningfulness (black)**: How relevant, substantive, and rich is the content they provide?
4. **Contextual Appropriateness (blue)**: How appropriate is the language in terms of register, audience, and social expectations?

For each ILR level (0, 0+, 1, 1+, 2, 2+, 3, 3+, 4, 4+, 5), provide:
- Whether the learner’s response meets that level’s criteria.
- Examples from the response illustrating this.
- Key gaps preventing advancement to the next level.
- Specific recommendations to address those gaps.

At the end, provide:
- The learner’s most accurate current ILR rating (0–5 or plus level).
- A clear learning roadmap with targeted practice recommendations.

---
Assessment Task:
{question}

Learner’s Response:
{learner_response}

Please structure your response level-by-level, using color-coded explanations (green for functional ability, red for precision issues, black for content quality, and blue for contextual appropriateness), and conclude with a professional recommendation.
"""
