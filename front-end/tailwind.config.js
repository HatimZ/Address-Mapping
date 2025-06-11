/** @type {import('tailwindcss').Config} */
import forms from '@tailwindcss/forms';
import typography from '@tailwindcss/typography';

export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				background: '#F8F8F6',
				card: '#FFFFFF',
				primary: '#222222',
				secondary: '#4B4949'
			},
			fontFamily: {
				inter: ['Inter', 'sans-serif']
			}
		}
	},
	plugins: [forms, typography]
};
