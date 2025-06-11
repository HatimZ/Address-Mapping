import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	preview: {
		allowedHosts: ['test-loadbalancer-1968215287.us-east-1.elb.amazonaws.com']
	}
});
