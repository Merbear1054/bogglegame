let score = 0;
let words = new Set();
let timer = 60;

// Show timer countdown
function showTimer() {
  $('#timer').text(timer);
}

// Send word to server
async function checkWord(word) {
  const res = await axios.get('/check-word', { params: { word } });
  return res.data.result;
}

// Handle word form submit
$('#word-form').on('submit', async function (evt) {
  evt.preventDefault();
  const $input = $('#word-input');
  const word = $input.val().toLowerCase();
  $input.val('');

  if (!word || words.has(word)) return;

  const result = await checkWord(word);

  if (result === 'ok') {
    words.add(word);
    score += word.length;
    $('#score').text(score);
    $('#msg').text(`✅ "${word}" is valid!`);
  } else if (result === 'not-on-board') {
    $('#msg').text(`❌ "${word}" is not on the board.`);
  } else {
    $('#msg').text(`❌ "${word}" is not a valid word.`);
  }
});

// Countdown timer
let countdown = setInterval(() => {
  timer--;
  showTimer();

  if (timer === 0) {
    clearInterval(countdown);
    $('#word-form').hide();
    endGame();
  }
}, 1000);

// Post score to backend
async function endGame() {
  const res = await axios.post('/post-score', { score });
  $('#high-score').text(res.data.high_score);
  $('#times-played').text(res.data.times_played);
  $('#msg').text(`⏱️ Time's up! Final score: ${score}`);
}
