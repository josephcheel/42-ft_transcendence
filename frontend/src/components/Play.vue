<template>
	<!-- <div>
	  <h1>Home Page</h1>
	  <p>Bienvenido a la página de inicio.</p>
	</div> -->
	<div class="container-fluid d-flex justify-content-center align-items-center " style="max-width: 400px; width: 100%;">
				<router-link id="play-button" class="btn btn-primary w-100" to="/select-game">{{ $t('message.links.play')}}!</router-link>
	</div>
</template>
<style >

#play-button {
	font-size: 40px !important;
}

</style>
<script>
	export default {
		data() {
			return {
				socket: null,
				message: '',
				receivedMessages: [],
			};
		},
		methods: {
			connect() {
				const ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
				const ws_path = ws_scheme + `://${this.$router.ORIGIN_IP}:8000/ws/gateway/`;

				this.socket = new WebSocket(ws_path);

				this.socket.onopen = () => {
					console.log("WebSocket connected");
				};

				this.socket.onmessage = (event) => {
					const data = JSON.parse(event.data);
					this.receivedMessages.push(data.message);
				};

				this.socket.onclose = () => {
					console.log("WebSocket disconnected");
				};
				this.socket.onerror = function(error) {
          		console.log('WebSocket Error: ', error);
        };
			},
			sendMessage() {
				if (this.socket && this.socket.readyState === WebSocket.OPEN) {
					this.socket.send(JSON.stringify({
						'message': this.message
					}));
					this.message = '';
				}
			}
		},
		mounted() {
			this.connect();
		}
	};

</script>


