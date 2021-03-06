"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");

let gameId;


/** Start */

async function start() {
  let response = await axios.get("/api/new-game");
  gameId = response.data.gameId;
  let board = response.data.board;

  displayBoard(board);
}

/** Display board */

function displayBoard(board) {
  $table.empty();

  for (let row of board) {
    let $tr = $("<tr>");
    for (let letter of row) {
      $tr.append(`<td>${letter}</td>`);
    }
    $table.append($tr);
  }
}

async function clickEvent(evt) {
  // prevent refresh of page
  evt.preventDefault()
  console.log('hi')
  // on click save value of input tag to variable
  const word = $wordInput.val().toUpperCase()

  // if input is empty return
  if (!word) return;
  // invoke submission to api, hardcode?
  submitWordToAPI(word);
  // reset from to empty when user clicks into
  $wordInput.val('').focus()

}

$form.on('submit', clickEvent)

async function submitWordToAPI(word) {
  let response = await axios.post('/api/score-word', {gameId: gameId, word: word})

  const result = response.data.result;
  // debugger;
  if (result === "not_a_word") {
    showMessage(`Not valid word: ${word}`, "err");
  } else if (result === "not_on_board") {
    showMessage(`Not on board: ${word}`, "err");
  } else {
    console.log('word valid')
    showWord(word);
    showMessage(`Added: ${word}`, "ok");
  }
}

async function showWord(word) {
  let $word = $(`<li>${word}</li>`)

  $playedWords.append($word);
}

function showMessage(msg, cssClass) {
  $message.text(msg).removeClass().addClass(`msg ${cssClass}`);

}

start();