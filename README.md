# Разработка прототипа чат-бота на основе HybridRAG для упрощения доступа к документам Национального управления архивов и документации США

Прототип представляет собой чат-бот для генерации ответов на запросы пользователя, реализующий технику **HybridRAG** с использованием **Neo4j** для построения графа знаний на основе **National Archives Catalog dataset**.

# Алгоритм создания KG

**Этап 1 — Подготовка**  
1.1. Импортируются необходимые библиотеки;  
1.2. Загружается модель для создания текстовых эмбеддингов.

**Этап 2 — Определение структуры данных**  
2.1. Определяются функции для обработки различных типов записей;  
2.2. Для каждого типа записи определяются соответствующие схемы для получения доступа к данным в JSON-структуре.

**Этап 3 — Обработка исходных данных**  
3.1. Извлекаются JSONL-файлы;  
3.2. Для каждой записи:  
- 3.2.1. Извлекаются основные данные согласно определенным схемам;  
- 3.2.2. Обрабатываются иерархические связи;  
- 3.2.3. Формируется текстовое поле;  
- 3.2.4. Длинные тексты разбиваются на чанки.

**Этап 4 — Создание узлов в графе**  
4.1. В соответствии со схемой для каждого узла создаются атрибуты на основе обработанных данных;  
4.2. Создаются ограничения для обеспечения уникальности `chunkId`.

**Этап 5 — Создание эмбеддингов**  
5.1. Создается экземпляр пользовательского класса `Embeddings`;  
5.2. Для всех узлов, содержащих текст, создаются эмбеддинги;  
5.3. Эмбеддинги сохраняются как атрибуты узлов для последующего семантического поиска;  
5.4. Создается векторный индекс для эффективного поиска.

**Этап 6 — Создание отношений между узлами**  
6.1. Создаются отношения с лейблом `Next` между чанками одного документа;  
6.2. Создаются отношения с лейблом `Includes` на основе информации об иерархических связях;  
6.3. Создаются дополнительные отношения между узлами на основе значений атрибута `naId`.

# Перечень атрибутов, создаваемых для каждого типа узлов

| **Entity** | **Properties** |
|-------------|----------------|
| item | file_name, line_num, ancestors, accessionNumbers, description_accessRestriction, note_accessRestriction, status_accessRestriction, audiovisual, beginCongress, authorityType_contributors, contributorType_contributors, heading_contributors, naId_contributors, logicalDate_coverageEndDate, logicalDate_coverageStartDate, custodialHistoryNote, groupName_dataControlGroup, dateNote, levelOfDescription, objectDescription_digitalObjects, objectType_digitalObjects, objectUrl_digitalObjects, endCongress, generalNotes, generalRecordsTypes, internalTransferNumbers, languages, localIdentifier, identifier_microformPublications, note_microformPublications, title_microformPublications, naId, description_onlineResources, note_onlineResources, url_onlineResources, otherTitles, partyDesignation, logicalDate_productionDates, recordsCenterTransferNumbers, recordType, scaleNote, scopeAndContentNote, authorityType_subjects, heading_subjects, naId_subjects, subtitle, title, transferNote, note_useRestriction, specificUseRestrictions_useRestriction, status_useRestriction, note_variantControlNumbers, number_variantControlNumbers, type_variantControlNumbers, copyStatus_physicalOccurrences, extent_physicalOccurrences, physicalOccurrenceNote_physicalOccurrences, text, chunkSeqId, chunkId, source |
| fileUnit | file_name, line_num, ancestors, accessionNumbers, description_accessRestriction, note_accessRestriction, status_accessRestriction, arrangement, audiovisual, beginCongress, authorityType_contributors, contributorType_contributors, heading_contributors, naId_contributors, logicalDate_coverageEndDate, logicalDate_coverageStartDate, custodialHistoryNote, groupName_dataControlGroup, dateNote, objectDescription_digitalObjects, objectType_digitalObjects, objectUrl_digitalObjects, editStatus, fileFormat_findingAids, findingAidtype_findingAids, note_findingAids, source_findingAids, url_findingAids, urlNote_findingAids, urlDescription_findingAids, endCongress, generalNotes, generalRecordsTypes, internalTransferNumbers, itemCount, languages, levelOfDescription, localIdentifier, naId, identifier_microformPublications, note_microformPublications, title_microformPublications, description_onlineResources, note_onlineResources, url_online_resources, otherTitles, partyDesignation, copyStatus_physicalOccurrences, extent_physicalOccurrences, physicalOccurrenceNote_physicalOccurrences, recordsCenterTransferNumbers, recordType, scaleNote, scopeAndContentNote, soundType, authorityType_subjects, heading_subjects, naId_subjects, subtitle, title, transferNote, note_useRestriction, specificUseRestrictions_useRestriction, status_useRestriction, note_variantControlNumbers, number_variantControlNumbers, type_variantControlNumbers, text, chunkSeqId, chunkId, source |
| series | file_name, line_num, ancestors, accessionNumbers, description_accessRestriction, note_accessRestriction, status_accessRestriction, arrangement, audiovisual, beginCongress, authorityType_contributors, contributorType_contributors, heading_contributors, naId_contributors, logicalDate_coverageEndDate, logicalDate_coverageStartDate, authorityType_creators, creatorType_creators, heading_creators, naId_creators, custodialHistoryNote, groupName_dataControlGroup, dateNote, dispositionAuthorityNumbers, editStatus, endCongress, fileUnitCount, fileFormat_findingAids, findingAidtype_findingAids, note_findingAids, source_findingAids, url_findingAids, urlNote_findingAids, functionAndUse, generalNotes, generalRecordsTypes, logicalDate_inclusiveEndDate, logicalDate_inclusiveStartDate, internalTransferNumbers, itemCount, languages, levelOfDescription, localIdentifier, identifier_microformPublications, note_microformPublications, title_microformPublications, naId, numberingNote, note_onlineResources, url_onlineResources, otherTitles, partyDesignation, copyStatus_physicalOccurrences, extent_physicalOccurrences, physicalOccurrenceNote_physicalOccurrences, recordsCenterTransferNumbers, recordType, scaleNote, soundType, authorityType_subjects, heading_subjects, naId_subjects, title, transferNote, note_useRestriction, specificUseRestrictions_useRestriction, status_useRestriction, note_variantControlNumbers, number_variantControlNumbers, type_variantControlNumbers, text, chunkSeqId, chunkId, source |
| recordGroup | file_name, line_num, beginCongress, logicalDate_coverageEndDate, logicalDate_coverageStartDate, groupName_dataControlGroup, dateNote, endCongress, fileFormat_findingAids, findingAidtype_findingAids, note_findingAids, source_findingAids, url_findingAids, urlNote_findingAids, logicalDate_inclusiveEndDate, logicalDate_inclusiveStartDate, levelOfDescription, naId, partyDesignation, recordGroupNumber, recordType, address1_referenceUnits, address2_referenceUnits, city_referenceUnits, email_referenceUnits, fax_referenceUnits, mailCode_referenceUnits, name_referenceUnits, phone_referenceUnits, postalCode_referenceUnits, state_referenceUnits, seriesCount, title, text, chunkSeqId, chunkId, source |
| collection | file_name, line_num, collectionIdentifier, logicalDate_coverageEndDate, logicalDate_coverageStartDate, groupName_dataControlGroup, dateNote, authorityType_donors, heading_donors, naId_donors, fileFormat_findingAids, findingAidtype_findingAids, note_findingAids, source_findingAids, url_findingAids, urlNote_findingAids, logicalDate_inclusiveEndDate, logicalDate_inclusiveStartDate, levelOfDescription, naId, recordType, address1_referenceUnits, address2_referenceUnits, city_referenceUnits, email_referenceUnits, fax_referenceUnits, mailCode_referenceUnits, name_referenceUnits, phone_referenceUnits, postalCode_referenceUnits, state_referenceUnits, seriesCount, title, note_variantControlNumbers, number_variantControlNumbers, type_variantControlNumbers, text, chunkSeqId, chunkId, source |
| geographicPlaceName | file_name, line_num, authorityType, description_broaderTerms, naId_broaderTerms, heading_broaderTerms, coordinates, heading, importRecordControlNumber, geographicPlaceName_linkCounts, jurisdiction_linkCounts, organization_linkCounts, subject_linkCounts, totalDescription_linkCounts, naId, naId_narrowerTerms, heading_narrowerTerms, naId_relatedTerms, heading_relatedTerms, recordSource, recordType, scopeNote, sourceNotes, useFor, text, chunkSeqId, chunkId, source |
| organization | file_name, line_num, administrativeHistoryNote, authorityType, naId_jurisdictions, name_jurisdictions, heading, contributor_linkCounts, creator_linkCounts, donor_linkCounts, subject_linkCounts, totalDescription_linkCounts, naId, contributorTypes_organizationNames, creatorTypes_organizationNames, heading_organizationNames, naId_organizationNames, name_organizationNames, recordSource_organizationNames, variantOrganizationNames, authorityType_personalReferences, heading_personalReferences, naId_personalReferences, programAreas, recordType, sourceNotes, text, chunkSeqId, chunkId, source |
| person | file_name, line_num, authorityType, biographicalNote, logicalDate_birthDate, logicalDate_deathDate, fullerFormOfName, heading, importRecordControlNumber, contributor_linkCounts, creator_linkCounts, donor_linkCounts, subject_linkCounts, totalDescription_linkCounts, naId, name, numerator, authorityType_organizationalReferences, heading_organizationalReferences, naId_organizationalReferences, personalTitle, recordSource, recordType, contributor_role, creator_role, donor_role, reference_role, sourceNotes, fullerFormOfName_variantPersonNames, heading_variantPersonNames, name_variantPersonNames, numerator_variantPersonNames, personalTitle_variantPersonNames, text, chunkSeqId, chunkId, source |
| specificRecordsTypes | file_name, line_num, authorityType, naId_broaderTerms, name_broaderTerms, heading, importRecordControlNumber, specificRecordsType_linkCounts, subject_linkCounts, totalDescription_linkCounts, naId, naId_narrowerTerms, heading_narrowerTerms, recordType, recordSource, naId_relatedTerms, heading_relatedTerms, scopeNote, sourceNotes, useFor, text, chunkSeqId, chunkId, source |
| topicalSubject | file_name, line_num, authorityType, naId_broaderTerms, name_broaderTerms, heading, subject_linkCounts, topicalSubject_linkCounts, totalDescription_linkCounts, naId, naId_narrowerTerms, heading_narrowerTerms, naId_relatedTerms, heading_relatedTerms, recordType, recordSource, scopeNote, sourceNotes, useFor, text, chunkSeqId, chunkId, source |

# Алгоритм работы чат-бота

**Этап 1 — Инициализация системы**  
1.1. Загружаются переменные окружения для подключения к Neo4j и Hugging Face;  
1.2. Определяется доступное вычислительное устройство (CPU/GPU);  
1.3. Загружаются две модели:  
- 1.3.1. Модель для создания эмбеддингов;  
- 1.3.2. Языковая модель для генерации ответов.

**Этап 2 — Настройка компонентов для работы**  
2.1. Создается экземпляр пользовательского класса `Embeddings`;  
2.2. Настраивается пайплайн для генерации текста.

**Этап 3 — Поиск релевантных документов**  
3.1. Формируется Cypher-запрос для поиска в графе Neo4j, с помощью которого:  
- 3.1.1. Находятся узлы с текстом, и расширяется контекст через отношения `Next`;  
- 3.1.2. Извлекается иерархическая структура записей через отношения `Includes`;  
- 3.1.3. Собираются связанные авторитетные записи.  

3.2. Создается векторное хранилище на основе существующего графа Neo4j;  
3.3. Используется семантический поиск по эмбеддингам для нахождения релевантных документов.

**Этап 4 — Классификация запроса пользователя и генерация ответа**  
4.1. Запрос пользователя классифицируется на два типа:  
- `show_records` — запрос на показ записей;  
- `question` — запрос, требующий ответа на основе контекста.  

4.2. Для запросов типа `show_records` формируется структурированный список найденных материалов;  
4.3. Для запросов типа `question`:  
- 4.3.1. Создается контекст из заголовков и текстов релевантных документов;  
- 4.3.2. Генерируется ответ со строгим ограничением использовать только информацию из контекста;  
- 4.3.3. При отсутствии ответа в контексте возвращается стандартное сообщение.

**Этап 5 — Форматирование и отображение результатов**  
5.1. Данные форматируются в виде диалоговых «пузырей»;  
5.2. Для каждого документа (при наличии соответствующих данных) формируется:  
- 5.2.1. Основная информация с датами и типом авторитетной записи;  
- 5.2.2. Список записей, стоящих выше в иерархии;  
- 5.2.3. Связанные авторитетные записи с кликабельными ссылками.

# retrieval_query

```python
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
```

# classification_prompt

```python
classification_prompt = """
Classify the type of user request. Reply with only one word:
- "question": if this is a question that needs an answer;
- "show_records": if the user is directly asking to display, list, show, etc.
archival materials/documents/full texts/records/sources.

If the request does NOT explicitly ask to display, list, show, etc., classify as
"question".

Examples:

Request: Why is the sky blue?
Output: question

Request: Show me documents about politics.
Output: show_records

Request: List the sources.
Output: show_records

Request: Give me all related documents.
Output: show_records

Request: Who was president in 1952?
Output: question
"""
```

# answer_prompt

```python
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
```