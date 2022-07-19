/**
 * @license
 * Copyright Google Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
const {google} = require('googleapis');
const fetch = require('node-fetch');
const express = require('express');
const app = express()
const bodyParser = require('body-parser');
app.use(bodyParser.json()); 
app.use(bodyParser.urlencoded({ extended: true }));



app.post('/', async (req, res) => {
  console.log("IN", req.body)
  handleCors(req, res);

  const url = `https://healthcare.googleapis.com/v1/projects/encoded-mark-356011/locations/us-central1/services/nlp:analyzeEntities`;
  let document;

  if (!req.body || !req.body.text) {
    res.status(200).send('No input text provided.');
  } else {
    console.log(`req.body ${JSON.stringify(req.body)}`);
    document = req.body.text;
  }

  const auth = new google.auth.GoogleAuth({
    keyFile: './key.json',
    scopes: ['https://www.googleapis.com/auth/cloud-healthcare'],
  });

  const accessToken = await auth.getAccessToken();
  const response = await fetch(url, {
    method: 'post',
    body: JSON.stringify({'document_content': document}),
    headers: {'Authorization': `Bearer ${accessToken}`, 'Content-Type': 'application/json'},
  });
  let json = await response.json();
  json['text'] = document;

  res.status(200).send(json);
});

/**
 * Sets up CORS to access in domains.
 */
handleCors = (req, res) => {
  res.set('Access-Control-Allow-Origin', '*');
  res.set('Access-Control-Allow-Methods', '*');
  res.set('Access-Control-Allow-Headers', 'access-control-allow-headers,access-control-allow-origin,authorization,content-type');
  res.set('Access-Control-Max-Age', '3600');
  if (req.method == 'OPTIONS') {
    res.status(204).send('');
  }
};


app.listen(3000);