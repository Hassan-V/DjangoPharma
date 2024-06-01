document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM loaded and parsed');
    // Check for a saved theme when the page loads
    if (localStorage.getItem('theme') === 'dark') {
      document.documentElement.classList.add('dark');
      document.querySelectorAll('.theme-toggle').forEach(function (button) {
        button.classList.add('justify-end');
      });
    } else if (localStorage.getItem('theme') === 'light') {
      document.documentElement.classList.remove('dark');
      document.querySelectorAll('.theme-toggle').forEach(function (button) {
        button.classList.remove('justify-end');
      });
    } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      document.documentElement.classList.add('dark');
      document.querySelectorAll('.theme-toggle').forEach(function (button) {
        button.classList.add('justify-end');
      });
    }
  
    // Toggle the theme and save the choice when the buttons are clicked
    var buttons = document.querySelectorAll('.theme-toggle');
    buttons.forEach(function (button) {
      button.addEventListener('click', function () {
        console.log('Button clicked');
        document.documentElement.classList.toggle('dark');
        button.classList.toggle('justify-end');
        localStorage.setItem('theme', document.documentElement.classList.contains('dark') ? 'dark' : 'light');
      });
    });
  
    // Mobile menu toggle
    document.getElementById('mobile-menu-button').addEventListener('click', function () {
      var mobileMenu = document.getElementById('mobile-menu');
      mobileMenu.classList.toggle('hidden');
    });
  
    // Handle mobile theme toggle
    document.getElementById('mobile-theme-toggle').addEventListener('click', function () {
      document.documentElement.classList.toggle('dark');
      this.classList.toggle('justify-end');
      localStorage.setItem('theme', document.documentElement.classList.contains('dark') ? 'dark' : 'light');
    });
  });
  