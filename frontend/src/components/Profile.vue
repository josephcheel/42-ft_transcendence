<template>
  <div class="card mx-auto" style="width: 18rem;">
    <!-- Mostrar la imagen o el campo de carga de archivo según el modo -->
    <div class="text-center mt-3" v-if="!isEditing">
      <img id="profile-picture" :src="user.profile_picture_url" class="rounded-circle img-fluid profile-picture" alt="User Image" />
    </div>
    <div class="mb-3" v-else>
      <label for="imageUpload" class="form-label">Profile Image</label>
      <input type="file" class="form-control" id="imageUpload" @change="onImageChange">
    </div>

    <div class="card-body">
      <h5 class="card-title text-center">{{ isEditing ? 'Edit Profile' : 'User Profile' }}</h5>

      <!-- Campos de información del usuario -->
      <div v-if="!isEditing">
        <p class="card-text"><strong>Name:</strong> {{ user.first_name }}</p>
        <p class="card-text"><strong>Last Name:</strong> {{ user.last_name }}</p>
        <p class="card-text"><strong>Username:</strong> {{ user.username }}</p>
        <p class="card-text"><strong>Tournament Username:</strong> {{ user.tournament_name }}</p>
      </div>

      <!-- Campos editables -->
      <div v-else>
        <div class="mb-3">
          <label for="firstName" class="form-label">First Name</label>
          <input type="text" class="form-control" v-model="user.first_name" id="firstName">
        </div>
        <div class="mb-3">
          <label for="lastName" class="form-label">Last Name</label>
          <input type="text" class="form-control" v-model="user.last_name" id="lastName">
        </div>
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input type="text" class="form-control" v-model="user.username" id="username">
        </div>
        <div class="mb-3">
          <label for="tournamentName" class="form-label">Tournament Username</label>
          <input type="text" class="form-control" v-model="user.tournament_name" id="tournamentName">
        </div>
      </div>

      <!-- Botón para alternar entre modo de edición y visualización -->
      <div class="text-center">
        <button class="btn btn-primary" @click="toggleEdit">
          {{ isEditing ? 'Save' : 'Edit' }}
        </button>
      </div>
    </div>
  </div>
</template>
<style scoped>
#profile-picture {
  width: 15vh;
  height: 15vh;
  border-radius: 50%;
  border: 3px solid black;
  object-fit: cover; /* Ensures the image covers the entire area */
  object-position: center; /* Centers the image */
  background-color: #f0f0f0; /* Placeholder background color */
}

#profile-picture::before {
  content: '';
  display: block;
  width: 100%;
  height: 100%;
  background-image: url('/profile_pictures/default.jpeg'); /* Placeholder image */
  background-size: cover;
  background-position: center;
  position: absolute;
  top: 0;
  left: 0;
  z-index: -1; /* Ensure the placeholder is behind the actual image */
}
</style>
<script>
import axios from '../utils/axiosConfig';
export default {
  data() {
    return {
      isEditing: false,
      user: {
        first_name: "",
        last_name: "",
        username: "",
        tournament_name: "",
        profile_picture_url: '/profile_pictures/default.jpeg',
      },
      selectedImage: null,
    };
  },
  mounted() {
    const username = localStorage.getItem('username');
    if (!username) {
      this.$router.push({ path: '/', params: { currentView: 'Login' } });
      // this.$router.push('/login'); // Redirigir al login si no está autenticado
    } else {
      
      this.fetchUserProfile();
    }
},

  methods: {
    toggleEdit() {
      if (this.isEditing){
        this.updateUserProfile();
        if (this.selectedImage){
          this.uploadProfilePicture();
        }
      }
      this.isEditing = !this.isEditing;
    },

    onImageChange(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.user.profile_picture_url = e.target.result; // Cambiar la imagen con la seleccionada
          this.selectedImage = file
        };
        reader.readAsDataURL(file);
      }
    },
    async fetchUserProfile() {
      const username = localStorage.getItem('username');
    
      if (!username) {
        console.error("No username found in localStorage");
        return; // Salir si no hay nombre de usuario
      }
      axios
        .get(`https://${this.$router.ORIGIN_IP}:8000/api/user/get_profile/${username}/`)
        .then((response) => {
          const data = response.data.data;
          // Asegurarse de que 'data' tenga las propiedades necesarias
          if (data) {
            this.user.first_name = data.first_name || '';
            this.user.last_name = data.last_name || '';
            this.user.username = data.username || '';
            this.user.tournament_name = data.tournament_name || '';
          } else {
            console.error("No user profile data received");
          }
        })

    axios
      .get(`https://${this.$router.ORIGIN_IP}:8000/api/user/get_profile_picture_url/${username}/`)
      .then((response) => {
        const pict = response.data.data;
        const url = pict.profile_picture_url;
        console.log("URL: " + url);
        this.user.profile_picture_url = url;
      })
      .catch((error) => {
        console.error("Error fetching user profile:", error.response ? error.response.data : error);
      });
    },
    async updateUserProfile() {
      try{
        await axios.post(`https://${this.$router.ORIGIN_IP}:8000/api/user/update_user/`, {
          first_name: this.user.first_name,
          last_name: this.user.last_name,
          username: this.user.username,
          tournament_name: this.user.tournament_name
        });
        console.log('User profile updated successfully.');
      } catch (error) {
        console.error("Error updating user profile:", error);
      }
    },

    async uploadProfilePicture() {
      const formData = new FormData();
      formData.append('picture', this.selectedImage);

      try {
        const response = await axios.post(`https://${this.$router.ORIGIN_IP}:8000/api/user/upload_picture/`, formData,);
        this.user.profile_picture_url = response.data.profile_picture_url;
        console.log('Profile picture uploaded successfully.');
      } catch (error) {
        console.error("Error uploading profile picture:", error);
      }
    }
  }
};
</script>
