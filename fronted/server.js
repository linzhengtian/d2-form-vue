const express = require('express')
const chalk = require('chalk')

const app = express()
const appPort = 8080

const history = require('connect-history-api-fallback')

app.use(history())

app.use(express.static('./'))
app.listen(appPort, function() {
  console.log(
    chalk.green(
      "启动完成(●'◡'●)ﾉ♥ ",
      chalk.underline('App listening on port: 8088')
    )
  )
})
