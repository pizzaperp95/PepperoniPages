package main

import (
	"strings"

	"github.com/gomarkdown/markdown"
	"github.com/gomarkdown/markdown/html"
	"github.com/gomarkdown/markdown/parser"

	"fmt"
	"log"
	"net/http"
	"os"
)

func remove(slice []string, s int) []string { // thanks stackoverflow user :3
	return append(slice[:s], slice[s+1:]...)
}

func peppagesHandler(response http.ResponseWriter, request *http.Request) {
	fmt.Fprintf(response, generatePage("../testing/pages/noelle.p2f"))
}

func generatePage(page string) string {
	data, err := os.ReadFile(page)
	if err != nil {
		return ""
	}

	md := []byte(parseP2F(string(data)))
	html := mdToHTML(md)

	return string(html)
}

func parseP2F(p2f string) string {
	var p2fLines []string
	var p2fReturn string

	p2fLines = strings.Split(p2f, "\n")
	var workingArray []string

	//mdstartFound := false
	for idx, line := range p2fLines {
		linesplit := strings.Split(line, " ")
		if strings.ToUpper(linesplit[0]) != "mdstart" {
			workingArray = remove(p2fLines, idx)
		} else {
			//mdstartFound = true
			workingArray = remove(p2fLines, idx)
		}
	}

	p2fLines = workingArray
	for _, line := range workingArray {
		p2fReturn = fmt.Sprintf("%s%s\n", workingArray, line)
		print(line, "\n")
	}
	return p2fReturn
}

func mdToHTML(md []byte) []byte { // this function is shamelessly stolen from the markdown parser github readme lol
	// create markdown parser with extensions
	extensions := parser.CommonExtensions | parser.AutoHeadingIDs | parser.NoEmptyLineBeforeBlock
	p := parser.NewWithExtensions(extensions)
	doc := p.Parse(md)

	// create HTML renderer with extensions
	htmlFlags := html.CommonFlags | html.HrefTargetBlank
	opts := html.RendererOptions{Flags: htmlFlags}
	renderer := html.NewRenderer(opts)

	return markdown.Render(doc, renderer)
}

func main() {

	// API routes

	// Serve files from static folder
	// http.Handle("/", http.FileServer(http.Dir("./cache")))
	// http.Handle("/", generatePage())

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		peppagesHandler(w, r)
	})

	port := ":5000"
	fmt.Println("PepperoniPages is running on port: " + port)

	// Start server on port specified above
	log.Fatal(http.ListenAndServe(port, nil))

}
