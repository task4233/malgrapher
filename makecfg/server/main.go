package main

import (
	"bytes"
	"encoding/base64"
	"image"
	"image/png"
	"io"
	"log"
	"net/http"
	"os"
	"os/exec"
	"text/template"
)

var templates = template.Must(template.ParseFiles("templates/index.html", "templates/show.html"))

func IndexHandler(w http.ResponseWriter, r *http.Request) {
	data := map[string]interface{}{"Title": "index"}
	renderTemplate(w, "index", data)
}

func UploadHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != "POST" {
		http.Error(w, "Allowed POST method only", http.StatusMethodNotAllowed)
		return
	}

	err := r.ParseMultipartForm(32 << 20) // maxMemory
	if err != nil {
		log.Println("failed ParseMultipartForm")
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	file, _, err := r.FormFile("upload")
	if err != nil {
		log.Println("failed FormFile")
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer file.Close()

	f, err := os.Create("./bin")
	if err != nil {
		log.Println("failed Create")
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer f.Close()

	io.Copy(f, file)

	err = exec.Command("make", "out").Run()
	if err != nil {
		log.Println("failed make out")
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	http.Redirect(w, r, "/show", http.StatusFound)
}

func ShowHandler(w http.ResponseWriter, r *http.Request) {
	file, err := os.Open("./cfg.png")
	defer file.Close()
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	img, _, err := image.Decode(file)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	writeImageWithTemplate(w, "show", &img)
}

func renderTemplate(w http.ResponseWriter, tmpl string, data interface{}) {
	if err := templates.ExecuteTemplate(w, tmpl+".html", data); err != nil {
		log.Fatalln("Unable to execute template.")
	}
}

func writeImageWithTemplate(w http.ResponseWriter, tmpl string, img *image.Image) {
	buffer := new(bytes.Buffer)
	if err := png.Encode(buffer, *img); err != nil {
		log.Fatalln("Unable to encode image.")
	}
	//	w.Header().Set("Content-Type", "image/jpeg")
	//	w.Header().Set("Content-Length", strconv.Itoa(len(buffer.Bytes())))
	//	if _, err := w.Write(buffer.Bytes()); err != nil {
	//		log.Println("unable to write image.")
	//	}
	str := base64.StdEncoding.EncodeToString(buffer.Bytes())
	data := map[string]interface{}{"Title": tmpl, "Image": str}
	renderTemplate(w, tmpl, data)
}

func main() {
	http.HandleFunc("/", IndexHandler)
	http.HandleFunc("/upload", UploadHandler)
	http.HandleFunc("/show", ShowHandler)
	http.ListenAndServe(":8888", nil)
}
