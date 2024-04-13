module.exports = {
    parser: require('postcss-scss'),
    plugins: [
        require('tailwindcss'),
        require('autoprefixer'),
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'), // updated line
        require('@tailwindcss/line-clamp'),
    ],
    content: [
        './main/templates/**/*.html',
        './main/static/js/**/*.js',
    ],
    theme: {
        extend: {},
    },
    variants: {},
}