const fetch = require('node-fetch');
const readline = require('readline');
const fs = require('fs');

module.exports = {
    mergefiles: function mergeFiles(url, file) {
        fetch(url)
            .then(res => res.text())
            .then(data => {
                fs.readFile('./src/api/parameters/quantuminteger.py', 'utf8', function (err, content) {
                    if (err) {
                        console.log(err);
                    } else {
                        fs.writeFile(file, content + data, (err) => {
                            if (err) console.log(err)
                            processLineByLine(file)
                        })
                    }
                })
            })
            .catch(err => { throw err; });
    }
}

async function processLineByLine(file) {
    const fileStream = fs.createReadStream(file);

    const rl = readline.createInterface({
        input: fileStream,
        crlfDelay: Infinity
    });
    // Note: we use the crlfDelay option to recognize all instances of CR LF
    // ('\r\n') in input.txt as a single line break.
    let i = 0;
    for await (const line of rl) {
        i++;
        // Each line in input.txt will be successively available here as `line`.
        //console.log(`Line from file: ${line}`);
        if (line.search('Circuit\\(\\)') != -1) {
            //let nline = line.search('Circuit')  //esto da la posicion en la linea, no el numero de linea, para eso hay que contar en el for con un contador
            //console.log(nline)

            let circuitName = line.toString().split('=');

            var data = fs.readFileSync(file).toString().split("\n");;
            data.splice(i, 0, "    prepareCircuit(" + circuitName[0] + ")");
            var text = data.join("\n");

            fs.writeFile(file, text, function (err) {
                if (err) return console.log(err);
            });
            break
        }
    }
}
