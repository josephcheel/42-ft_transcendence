<template>
  <div class="card mx-auto mt-3" style="width: 18rem;">
    <!-- Mostrar la imagen o el campo de carga de archivo según el modo -->
    <div class="text-center mt-3" v-if="!isEditing">
      <img id="profile-picture" :src="user.profile_picture_url" class="rounded-circle img-fluid profile-picture" alt="User Image" />
    </div>
    <div class="mb-3" v-else>
      <label for="imageUpload" class="form-label">{{ $t('general.picprofile')}}</label>
      <input type="file" class="form-control" id="imageUpload" @change="onImageChange">
    </div>

    <div class="card-body">
      <h5 class="card-title text-center">{{ isEditing ? $t('general.edit_profile') : $t('general.user_profile') }}</h5>

      <!-- Campos de información del usuario -->
      <div id="info" v-if="!isEditing" >
        <p class="form-label"><strong>{{ $t('general.name')}}</strong> {{ user.first_name }}</p>
        <p class="form-label"><strong>{{ $t('general.lastname')}}</strong> {{ user.last_name }}</p>
        <p class="form-label"><strong>{{ $t('general.username')}}</strong> {{ user.username }}</p>
        <p class="form-label"><strong>{{ $t('general.username_tournament')}}</strong> {{ user.tournament_name }}</p>
        <p class="form-label"><strong>{{ $t('general.language') }}</strong> {{ user.lang_text }}</p>
      </div>

      <!-- Campos editables -->
      <div v-else>
        <div class="mb-3">
          <label for="firstName" class="form-label">{{ $t('general.name')}}</label>
          <input type="text" class="form-control" v-model="user.first_name" id="firstName">
        </div>
        <div class="mb-3">
          <label for="lastName" class="form-label">{{ $t('general.lastname')}}</label>
          <input type="text" class="form-control" v-model="user.last_name" id="lastName">
        </div>
        <div class="mb-3">
          <label for="tournamentName" class="form-label">{{ $t('general.username_tournament')}}</label>
          <input type="text" class="form-control" v-model="user.tournament_name" id="tournamentName">
        </div>
        <div class="mb-3">
          <label for="lang" class="form-label">{{ $t('general.language') }}</label>
          <div class="dropdown-menu" style="display: block; position: relative; display: flex; flex-direction: column; left: 10%; top:0%;">
            <a class="dropdown-item" :class="{ active: user.lang === 'en' }" @click="changeLang('en');">English</a>
            <a class="dropdown-item" :class="{ active: user.lang === 'es' }" @click="changeLang('es');">Español</a>
            <a class="dropdown-item" :class="{ active: user.lang === 'fr' }" @click="changeLang('fr');">Français</a>
          </div>
        </div>
      </div>

      <!-- Botón para alternar entre modo de edición y visualización -->
      <div v-if="editProfile" class="text-center" style="position: absolute;
      bottom: 0;
        left: 40%;">
        <button class="btn btn-primary" @click="toggleEdit">
          {{ isEditing ? 'Save' : 'Edit' }}
        </button>
      </div>
    </div>
  </div>
</template>
<style scoped>

.text-center {
  display: flex !important;
  justify-content: center !important;
  align-items: center !important;
  
}
.btn-primary {
  font-size: 0.8rem !important;
  height: fit-content;
}

#profile-picture {
  width: 15vh;
  height: 15vh;
  border-radius: 50%;
  /* border: 3px solid black; */
  border : 3px solid rgba(255, 255, 255, 0.391);
  object-fit: cover; /* Ensures the image covers the entire area */
  object-position: center; /* Centers the image */
  background-color: #f0f0f0; /* Placeholder background color */
}

.card {
  background-color: rgba(255, 255, 255, 0.379) !important;
}

.card-title {
  font-size: 1.5rem;
  font-weight: bold;
}


.form-label {
  color: black !important;
  font-size: small !important;
  font-family: 'Roboto' !important;
}
#info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
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
        profile_picture_url: "/assets/images/default-profile.jpeg",
        lang: "",
        lang_text: ""
      },
      selectedImage: null,
    };
  },
  mounted() {
    const username = localStorage.getItem('username');
    if (!username) {
      this.$router.push({ path: '/', params: { currentView: 'Login' } });
    } else {
      this.fetchUserProfile();
    }
},
  props: {
    editProfile: {
      type: Boolean,
      required: true,
      default: true
    },
    username: {
      type: String,
      required: false,
      default: ''
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

    changeLang(lang){
      this.user.lang = lang;
    },
    changeLangText(){
      if(this.user.lang === "en")
        this.user.lang_text = "English"
      else if(this.user.lang === "fr")
        this.user.lang_text = "Français"
      if(this.user.lang === "es")
        this.user.lang_text = "Español"
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
      if (this.username) {
        this.user.username = this.username;
      } else {
       this.user.username = localStorage.getItem('username');
       if (!this.user.username) {
         console.error("No username found in localStorage");
         return; // Salir si no hay nombre de usuario
       }
      }
      axios
        .get(`https://${this.$router.ORIGIN_IP}:8000/api/user/get_profile/${this.user.username}/`)
        .then((response) => {
          const data = response.data.data;
          console.log("User profile data:", data);
          // Asegurarse de que 'data' tenga las propiedades necesarias
          if (data) {
            this.user.first_name = data.first_name || '';
            this.user.last_name = data.last_name || '';
            this.user.username = data.username || '';
            this.user.tournament_name = data.tournament_name || '';
            this.user.lang = data.lang || '';
            this.changeLangText()
          } else {
            console.error("No user profile data received");
          }
        })

    axios
      .get(`https://${this.$router.ORIGIN_IP}:8000/api/user/get_profile_picture_url/${this.user.username}/`)
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
          tournament_name: this.user.tournament_name,
          language: this.user.lang
        });
        console.log('User profile updated successfully.');
        this.$i18n.locale = this.user.lang;
        this.changeLangText()
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
        window.location.reload();
      } catch (error) {
        console.error("Error uploading profile picture:", error);
      }
    }
  }
};
</script>
