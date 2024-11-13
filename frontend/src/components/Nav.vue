<template>
	<nav class="navbar navbar-expand-lg">
	  <div class="container-fluid">
		<router-link to="/play">
		<img id="title" src="/assets/images/PONG3D.png" alt="Logo">
		</router-link>
		<button
		  class="navbar-toggler"
		  type="button"
		  data-bs-toggle="collapse"
		  data-bs-target="#navbarNav"
		  aria-controls="navbarNav"
		  aria-expanded="false"
		  aria-label="Toggle navigation"
		>
		  <span class="navbar-toggler-icon"></span>
		</button>
		<div class="collapse navbar-collapse" id="navbarNav">
		  <ul class="navbar-nav ms-auto">
			<li class="nav-item">
				<router-link :class="`nav-link ${isActive('/play')}`" to="/play" aria-current="page">{{ $t('message.links.home') }}</router-link>
			  <!-- <a :class="`nav-link ${isActive('/play')}`"  aria-current="page" href="/play">{{ $t('message.links.home')}}</a> -->
			</li>
			<li class="nav-item">
				<router-link :class="`nav-link ${isActive('')}`" to="/stats">{{ $t('message.links.stats') }}</router-link>
			</li>
			<li class="nav-item">
				<router-link :class="`nav-link ${isActive('')}`" to="/history">{{ $t('message.links.history') }}</router-link>
			</li>
			<li class="nav-item">
				<router-link :class="`nav-link ${isActive('/select-game')}`" to="/select-game">{{ $t('message.links.games') }}</router-link>
			</li>
			<li class="nav-item">
				<router-link :class="`nav-link ${isActive('/friends')}`" to="/friends">{{ $t('message.links.friends') }}</router-link>
			</li>
			<li class="nav-item dropdown">
				<a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
					Language
				</a>
				<ul class="dropdown-menu" aria-labelledby="navbarDropdown" >
					<li><a class="dropdown-item" @click="changeLang('en');">English</a></li>
					<li><a class="dropdown-item" @click="changeLang('es');">Español</a></li>
					<li><a class="dropdown-item" @click="changeLang('fr')">Français</a></li>
					<!-- Add more languages here -->
				</ul>
			</li>
			
			<li id="user-info" class="nav-item d-flex justify-content-center">
				<div class="row text-center">
					<div class="col-12">
						{{ points }} <img id="trophy" src="/assets/icons/feed-trophy.svg" alt="Points" width="20" height="20">
					</div>
					<div class="col-12">
						{{ username }}
					</div>
				</div>
			</li>
		</ul>
		




		<div class="navbar-item dropdown"  id="profileDropdown" aria-labelledby="navbarDropdown">
			<a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
				<img :src="profile_picture_url" alt="Profile Picture" class="rounded-circle" width="50" height="50">
			</a>
			<ul class="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdown">
				<li><router-link :class="`dropdown-item ${isActive('')}`" to="/profile">{{ $t('message.links.profile') }}</router-link></li>
				<li><router-link :class="`dropdown-item ${isActive('')}`" to="/settings">{{ $t('message.links.settings') }}</router-link></li>
				<li><a class="dropdown-item" @click="logout">{{ $t('message.links.logout')}}</a></li>
			</ul>
		</div>

		</div>
	  </div>
	</nav>
  </template>
  <style scoped>
  .rounded-circle {
	border : 2px solid rgba(255, 255, 255, 0.391);
  }
  #trophy {
		padding-bottom: 4px;
	}
  .col-12 {

	padding: 0px;
  }
  .dropdown-item{
	cursor: pointer;
  }
  #user-info {
	  font-size: 0.6rem;
	  /* margin-right: 0.5em; */
	  padding: 0px;
	  padding-right: 15px;
	  padding-left: 15px;
	  display: flex;
	  /* justify-content: right !important; */
	  align-items:center;

  }
  .navbar {
	font-family: 'Nokia Cellphone FC';
	font-size: 0.7rem;
	/* background: #FF9670; */
	/* background: linear-gradient(90deg, #ffe0b4 0%, #ff9797 100%); */
	/* background: #8dcaff; */
	background: #ffbe82; 
	box-shadow: 0 5px 6px rgba(0, 0, 0, 0.1); 
	margin-left: 10px;
	margin-right: 10px;
	margin-top: 10px;
	display: flex;
	align-items: center;
	justify-content: space-between;
	border-radius: 5px;
  }
  .dropdown-menu
  {
		font-size: 0.6rem;
  }
  #title {
	width: 150px;
	height: auto;
  }
	/* Ensure the profile dropdown is centered */
	#profileDropdown {
	display: flex;
	justify-content: center;
	align-items: center;
	}

	/* Optionally, you can also ensure the image itself is centered within the anchor tag */
	#profileDropdown .dropdown-toggle {
	display: flex;
	justify-content: center;
	align-items: center;
	}

	/* You can also tweak the image styling */
	#profileDropdown img {
	width: 50px;
	height: 50px;
	object-fit: cover;  /* Ensures the image is cropped to fit the size */
	}

  </style>
  <script>
 import axios from '../utils/axiosConfig'; 
  export default {
	name: "NavBar",
	props: {
		username: { type: String, required: true },
		points: { type: Number, required: true },
		profile_picture_url: { type: String, required: true },
	},
	computed: {
		currentRoute() {
		return this.$route.path; // This requires Vue Router to be configured
		}
	},
	
	async mounted() {
	  while (!localStorage.getItem('username') || !localStorage.getItem('points')) {
		await new Promise(resolve => setTimeout(resolve, 100));
	  }
	  this.username = localStorage.getItem('username'); 
	  this.points = localStorage.getItem('points');
	  this.getProfilePicture();
	},
	methods: {
		changeLang(selectedLang) {
        this.$i18n.locale = selectedLang;
      },
	  isActive(route) {
      	return this.currentRoute === route ? 'active' : '';
    	},
	async getProfilePicture() {
		console.log("Fetching profile picture in Nav");
	axios
		.get(`https://${this.$router.ORIGIN_IP}:8000/api/user/get_profile_picture_url/${this.username}/`)
		.then((response) => {
			const pict = response.data.data;
			const url = pict.profile_picture_url;
			console.log("URL: " + url);
			this.profile_picture_url = url;
		})
		.catch((error) => {
			console.error("Error fetching user profile:", error.response ? error.response.data : error);
		});
	},
	logout() {
        axios.post(`https://${this.$router.ORIGIN_IP}:8000/api/user/logout_user/`).then((response) => {
          if (response.status === 200)
          {
			this.$router.push('/');
			console.log(response);
          }
          else
          {
            console.log(response);
          }
        });
      },
	},
  };
  </script>