retrieval_query = """
MATCH (node:recordWithText)
CALL (node) {
    MATCH window = (:recordWithText)-[:Next*0..1]->(node)-[:Next*0..1]->(:recordWithText)
    WITH window
    ORDER BY length(window) DESC
    LIMIT 1
    RETURN window AS longestWindow
}
WITH node, score, longestWindow
WITH nodes(longestWindow) AS chunkList, node, score
UNWIND chunkList AS chunkRows
WITH collect(chunkRows.text) AS textList, node, score
MATCH (firstNode)
WHERE firstNode.naId = node.naId AND firstNode.chunkSeqId = 0
OPTIONAL MATCH path = (root)-[:Includes*0..]->(firstNode)
WHERE NOT (root)<-[:Includes]-()
OPTIONAL MATCH (relatedNode)-[
    :broaderTerm
    |:contributor
    |:creator
    |:subject
    |:donor
    |:narrowerTerm
    |:organizationalReference
    |:relatedTerm
    |:jurisdiction
    |:organizationName
    |:personalReference
]->(firstNode)
WITH
    textList, node, score,
    COLLECT(DISTINCT relatedNode {.authorityType, .heading, .source}) AS relatedAuthorities,
    firstNode,
    path
WITH
    textList, node, score, relatedAuthorities,
    CASE firstNode.recordType
        WHEN 'description' THEN 
            [n IN reverse(nodes(path)) | n {
                .recordType,
                .levelOfDescription,
                .title,
                .logicalDate_coverageStartDate,
                .logicalDate_coverageEndDate,
                .source
            }]
        WHEN 'authority' THEN
            [n IN nodes(path) | n {
                .recordType,
                .authorityType,
                .heading,
                .source
            }]
    END AS pathNodes
RETURN
    apoc.text.join(textList, "\n") AS text,
    score,
    {
        path_nodes: pathNodes, 
        score: score,
        related_authorities: relatedAuthorities
    } AS metadata
"""