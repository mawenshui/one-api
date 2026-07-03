package cohere

var ModelList = []string{
	// 6 个原版(自动加 -internet 变体)
	"command", "command-nightly",
	"command-light", "command-light-nightly",
	"command-r", "command-r-plus",
	// v4 新增
	"command-r-08-2024", "command-r-plus-08-2024",
	"command-a-03-2025", "command-a",
	"command-light-nightly",
	"c4ai-aya-expanse-8b", "c4ai-aya-expanse-32b",
	"embed-english-v3.0", "embed-english-light-v3.0",
	"embed-multilingual-v3.0", "embed-multilingual-light-v3.0",
	"rerank-english-v3.0", "rerank-multilingual-v3.0",
}

func init() {
	num := len(ModelList)
	for i := 0; i < num; i++ {
		ModelList = append(ModelList, ModelList[i]+"-internet")
	}
}
