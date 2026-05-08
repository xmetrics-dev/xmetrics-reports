<!DOCTYPE html>
<html lang="en">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-J8MZYC2F8C"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-J8MZYC2F8C');
</script>
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-5MWMJW4J');</script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>xmetrics — AI Hedge Fund</title>
    <link rel="icon" href="/favicon.ico" sizes="32x32">
    <link rel="icon" href="img/icon.svg" type="image/svg+xml">
    <link rel="apple-touch-icon" href="img/icon.png">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;800&family=JetBrains+Mono:wght@300;400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="css/landing.css">
    <script src="https://cdn.jsdelivr.net/npm/tsparticles@2.12.0/tsparticles.bundle.min.js"></script>
    <script src="js/tsparticles.js" defer></script>
</head>
<body>
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-5MWMJW4J"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>

    <div id="tsparticles"></div>

    <div class="ui-element top-left">
     <img src="img/logo.svg" width="130">
    </div>

    <div class="ui-element top-right">
        <nav class="top-nav">
            <a href="/dokumentace">Dokumentace</a>
            <a href="/metriky">Metriky</a>
            <a href="/o-projektu">O projektu</a>
            <a href="https://x.com/xmetrics_cz" target="_blank"><img src="img/x-icon.svg" width="20"></a>
            <a href="https://github.com/xmetrics-dev/xmetrics-reports" target="_blank"><img src="img/github.svg" width="24"></a>
        </nav>
    </div>

    <main class="container">
        <div class="left-column">
            <h1 class="hero-title">Analyzuj S&P 500</br> jako Hedge fund</h1>
            <div class="hero-description">Multi-agent AI framework, který analyzuje 100 tržních metrik optikou Markse, Druckenmillera, Damodarana, Taleba a experta technické analýzy, zakončený CIO syntézou se závěrečným verdiktem.
            </div>

<a href="login.php" class="dashboard-btn">
            Dashboard
        </a>
        </div>

        <div class="right-column">
            <div class="footer-links">
                <a href="privacy.php">Ochrana soukromí</a>
                <span class="sep">|</span>
                <a href="terms.php">Podmínky</a>
                <span class="sep">|</span>
                <button type="button" class="contact-trigger" data-open-contact>Kontakt</button>
            </div>
        </div>
    </main>

    <!-- Contact modal -->
    <div class="modal-overlay" id="contactModal" role="dialog" aria-modal="true" aria-labelledby="contactLabel">
        <div class="modal">
            <button type="button" class="modal-close" aria-label="Close" data-close-contact>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                    <path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
                </svg>
            </button>
            <div class="modal-label" id="contactLabel">Kontakt pro podporu nebo partnerství:</div>
            support@xmetrics.dev
        </div>
    </div>

  <script>
        (function () {
            var modal = document.getElementById('contactModal');
            var openers = document.querySelectorAll('[data-open-contact]');
            var closers = document.querySelectorAll('[data-close-contact]');

            function openModal() { modal.classList.add('is-open'); }
            function closeModal() { modal.classList.remove('is-open'); }

            openers.forEach(function (el) {
                el.addEventListener('click', function (e) { e.preventDefault(); openModal(); });
            });
            closers.forEach(function (el) {
                el.addEventListener('click', closeModal);
            });
            modal.addEventListener('click', function (e) {
                if (e.target === modal) closeModal();
            });
            document.addEventListener('keydown', function (e) {
                if (e.key === 'Escape') closeModal();
            });
        })();
    </script>

</body>
</html>
