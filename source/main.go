package main

import (
	"errors"
	"slices"
	"strings"

	"github.com/h2non/filetype"

	"github.com/gomarkdown/markdown"
	"github.com/gomarkdown/markdown/html"
	"github.com/gomarkdown/markdown/parser"

	"fmt"
	"log"
	"net/http"
	"os"
)

var templatePath string = ""
var serverRoot string = "../server"
var serverPaths = []string{"static", "cache", "pages"}

func remove(arr []string, s int) []string {
	var newArr []string
	for idx, line := range arr {
		if idx != s {
			newArr = append(newArr, line)
		}
	}
	return newArr
}

func getMime(fileExt string) string {
	//fmt.Println(fileExt)
	switch fileExt {
	case "css":
		return "text/css"
	case "js":
		return "application/javascript"
	default:
		return "text/plain"
	}
}

func getFileDirectoryAndType(response http.ResponseWriter, request *http.Request) {
	var filePath string = ""
	var fileFound bool = false
	var fileExt string
	var fileName string
	var fileTypeIsPage bool = false
	//var returnStr string = ""
	//var fileFoundDir string
	var fileFoundPath string
	var foundFileExt string

	if request.URL.Path[len(request.URL.Path)-1:] == "/" {
		filePath = (request.URL.Path + "/index")
	} else {
		filePath = request.URL.Path
	}

	var splitPath []string = strings.Split(filePath, "/")

	if len(strings.Split(splitPath[len(splitPath)-1], ".")) == 2 {
		fileExt = strings.Split(splitPath[len(splitPath)-1], ".")[1]
	} else {
		fileExt = ""
	}

	if fileExt == "" || fileExt == "html" {
		fileTypeIsPage = true
	}

	fileName = strings.Split(splitPath[len(splitPath)-1], ".")[0]
	fmt.Println("fileext: ", fileExt, " filename: ", fileName)

	var pathNoExt []string
	var pathNoExtStr string
	for _, seg := range splitPath {
		if len(strings.Split(seg, ".")[0]) > 0 {
			pathNoExt = append(pathNoExt, strings.Split(seg, ".")[0])
			pathNoExtStr = strings.Join([]string{pathNoExtStr, strings.Split(seg, ".")[0]}, "/")
		}
	}

	//fmt.Println(pathNoExt, pathNoExtStr)

	for _, seg := range serverPaths {
		fmt.Println(seg)
		var workingExt string
		if fileTypeIsPage {
			workingExt = "html"
			if seg == "pages" {
				workingExt = "p2f"
			}
		} else {
			workingExt = fileExt
		}
		//fmt.Println(serverRoot + "/" + seg + pathNoExtStr + "." + workingExt)
		if _, err := os.Stat(serverRoot + "/" + seg + pathNoExtStr + "." + workingExt); err == nil {
			fileFound = true
			//fileFoundDir = seg
			foundFileExt = workingExt
			fileFoundPath = serverRoot + "/" + seg + pathNoExtStr + "." + workingExt
			break

		} else if errors.Is(err, os.ErrNotExist) {
			fileFound = false
		} else {
			fileFound = false
		}
	}

	if !fileFound {
		http.Error(response, reqErr404(), http.StatusNotFound)
		fmt.Fprintf(response, reqErr404())
		return
	} else {
		if fileTypeIsPage {
			if foundFileExt == "p2f" {
				fmt.Fprintf(response, generatePage(fileFoundPath))
			} else {
				data, err := os.ReadFile(fileFoundPath)
				if err != nil {
					return
				}
				fmt.Fprintf(response, string(data))

			}

		} else {
			data, err := os.ReadFile(fileFoundPath)
			if err != nil {
				return
			}
			kind, _ := filetype.Match(data)
			response.Header().Set("Content-Type", getMime(fileExt))
			if kind == filetype.Unknown {
				response.Write(data)
				//fmt.Fprintf(response, string(data))
			} else {
				response.Write(data)
			}
			response.Write(data)
			//fmt.Fprintf(response, string(data))
		}
	}
	//fmt.Println(fileFoundDir)
	return
}

func reqErr404() string {
	errMsg := ""
	var returnPath string = serverRoot + "/static/404.html"
	data, err := os.ReadFile(returnPath)
	if err != nil {
		errMsg = http.StatusText(http.StatusNotFound)
	} else {
		errMsg = string(data)
	}

	return errMsg
}

func peppagesHandler(response http.ResponseWriter, request *http.Request) {
	//fmt.Println(request.URL.Path)
	//response.Header().Set("Content-Type", "text/html")
	getFileDirectoryAndType(response, request)
	//fmt.Fprintf(response, generatePage())

}

func generatePage(page string) string {
	data, err := os.ReadFile(page)
	if err != nil {
		return ""
	}

	var md []byte = []byte(parseP2F(string(data)))
	var html []byte = mdToHTML(md)
	var pageOut string = insertIntoTemplate(string(html))
	fmt.Println(pageOut)
	return pageOut
}

func insertIntoTemplate(html string) string {
	var realTemplatePath string = serverRoot + "/templates/" + templatePath
	data, err := os.ReadFile(realTemplatePath)
	if err != nil {
		fmt.Printf("Template file \"%s\" not found.\n", realTemplatePath)
		return html
	}
	var templateString string = string(data)
	var templateArr = strings.Split(templateString, "\n")
	var peppagesIdx int
	for idx, line := range templateArr {
		noWhitespace := strings.ReplaceAll(line, " ", "")
		if noWhitespace == "<pepperonipages>" {
			peppagesIdx = idx
		}

	}
	var arrTemp []string = remove(templateArr, peppagesIdx)
	var arrOut []string = slices.Insert(arrTemp, peppagesIdx, html)

	var strOut string
	for _, line := range arrOut {
		strOut = fmt.Sprintf("%s%s\n", strOut, line)
	}
	return strOut
}

func stripTags(lines *[]string) *[]string {
	var workingArray []string = *lines
	mdstartFound := false
	fileFinished := false
	for {

		for idx, line := range workingArray {
			linesplit := strings.Split(line, " ")
			tag := strings.ToLower(strings.Split(linesplit[0], "=")[0])
			if tag == "mdstart" {
				workingArray = remove(workingArray, idx)
				mdstartFound = true
				break
			} else if tag == "p2formatver" {
				workingArray = remove(workingArray, idx)
				break
			} else if tag == "mdend" {
				workingArray = remove(workingArray, idx)
				break
			} else if tag == "template" {
				templatePath = strings.Split(linesplit[0], "=")[1]
				workingArray = remove(workingArray, idx)
				break
			} else if !mdstartFound {
				workingArray = remove(workingArray, idx)
			}
			if idx == len(workingArray)-1 {
				fileFinished = true
			}
		}

		if fileFinished {
			break
		}
	}
	// for idx, line := range workingArray {
	// 	linesplit := strings.Split(line, " ")
	// 	tag := strings.ToLower(strings.Split(linesplit[0], "=")[0])
	// 	if tag == "mdstart" {
	// 		workingArray = remove(workingArray, idx)
	// 		mdstartFound = true
	// 	}
	// 	if tag == "p2formatver" || tag == "mdend" {
	// 		workingArray = remove(workingArray, idx)
	// 	}
	// 	if mdstartFound == false {
	// 		fmt.Println("meow")
	// 	}
	// }
	return &workingArray

}

func parseP2F(p2f string) string {
	templatePath = ""
	var p2fLines []string
	var p2fReturn string

	p2fLines = strings.Split(p2f, "\n")
	var workingArray []string

	workingArray = *stripTags(&p2fLines)

	for _, line := range workingArray {
		p2fReturn = fmt.Sprintf("%s%s\n", p2fReturn, line)
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
	//fmt.Println(string(markdown.Render(doc, renderer)))
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
