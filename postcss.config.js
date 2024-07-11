// postcss.config.js
module.exports = {
    parser: require('postcss-scss'),
    plugins: [
        require('tailwindcss'),
        require('autoprefixer'),
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
        require('@tailwindcss/line-clamp'),
    ],
    content: [
        './central/templates/**/*.html',
        './central/static/js/**/*.js',
    ],
    theme: {
        extend: {},
    },
    variants: {},
}