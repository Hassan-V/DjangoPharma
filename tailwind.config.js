// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './central/templates/**/*.html',
    './central/static/js/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          light: '#bfdbfe', // Light blue
          DEFAULT: '#3b82f6', // Blue
          dark: '#1e3a8a', // Dark blue
        },
      },
    },
  },
  plugins: [],
  darkMode: 'class',
};
