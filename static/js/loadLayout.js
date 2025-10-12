async function loadLayout() {
  // Cargar header
  const headerResponse = await fetch('header.html');
  const headerHTML = await headerResponse.text();
  document.getElementById('header').innerHTML = headerHTML;

  // Cargar footer
  const footerResponse = await fetch('footer.html');
  const footerHTML = await footerResponse.text();
  document.getElementById('footer').innerHTML = footerHTML;


}

loadLayout();
