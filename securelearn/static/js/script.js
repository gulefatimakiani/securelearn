<script>
  

document.addEventListener('DOMContentLoaded', function () {
    animateCards();
});


function animateCards() {
    var cards = document.querySelectorAll('.card');
    cards.forEach(function (card) {
        card.classList.add('show');
    });
}
</script>