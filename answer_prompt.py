answer_prompt = """
Answer the question based ONLY on the provided context.
Use ONLY information and wording from the context.
Do NOT add information that is not explicitly stated in the context,
even if it seems logical or obvious.
Do NOT include extra information that is present in the context but is not
directly relevant to the question.
If the context doesn't contain an answer to the question, say "I cannot
respond to your request based on the available archival materials."
Answer in one or maximum two sentences.

Examples:

Context: Title: Discussion with Congressman Y Text: Congressman Y talked
about his role in a particular panel, highlighting that the working groups
operate with significant autonomy. He mentioned that the responsibilities are
extremely intensive, hindering participants from adequately participating in
additional congressional tasks and attending to their constituencies.
Question: What did Congressman Y say about the panel's workload?
Answer: Congressman Y said the responsibilities are extremely intensive,
hindering participants from adequately participating in additional
congressional tasks and attending to their constituencies.

Context: Title: Interview with Legislator B Text: The speaker indicated
a preference for a collaborative dynamic with federal bureaus, involving
mutual idea-sharing. Conversely, he portrayed a fellow lawmaker, Mr. Q, who
often employs aggressive rhetoric and harbors suspicion toward these entities.
Question: How does the Legislator B's method with bureaus contrast with Mr. Q's?
Answer: Legislator B favors collaboration and mutual idea-sharing, whereas Mr.
Q employs aggressive rhetoric and shows suspicion.

Context: Title: Dialogue with Lawmaker C Text: Lawmaker C pointed out that
an individual with intense personal stakes in a specific issue domain ought not
to be placed on the task force overseeing it, since they might lack
impartiality.
Question: According to Lawmaker C, what kind of individual should avoid
placement on a task force?
Answer: An individual with intense personal stakes in a specific issue domain
should not be placed on the task force overseeing it, as they might lack
impartiality.

Context: Title: Study Notes on a Task Force Text: The document describes
assignment to a particular task force as a secondary role due to its divisive
nature. It emphasizes that participants should secure an additional, more
favorable position as well.
Question: Why is assignment to this task force viewed as a secondary role?
Answer: It is viewed as a secondary role due to its divisive nature, and the
document emphasizes that participants should secure an additional, more
favorable position.

Context: Title: Meeting with Senator Z Text: Senator Z discussed the
procedural hurdles in forming a bipartisan committee, noting that scheduling
conflicts among senior members have caused significant delays. He expressed
hope that the committee would be operational by the next fiscal quarter.
Question: What views did Senator Z express about tax reforms?
Answer: I cannot respond to your request based on the available archival
materials.
"""