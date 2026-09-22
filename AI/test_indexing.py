from AI.indexing_agent import IndexingAgent


agent = IndexingAgent()

result = agent.index_project(".")

print("Project:", result["project_name"])
print("Files:", result["file_count"])

for file in result["files"]:
    print(file)