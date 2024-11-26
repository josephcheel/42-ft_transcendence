<template>
<div class="container my-5">
        <div class="row">
            <!-- First Column -->
            <div class="col-md-9 col-12 order-2 order-md-1">
				<Gamestats 
				:username="this.$route.params.username"
				/>
            </div>
            <!-- Second Column -->
            <div class="col-md-3 col-12 order-1 order-md-2">
				<Profile 
					:username="this.$route.params.username"
					:editProfile="editProfile"
				/>
            </div>
        </div>
    </div>
</template>
<script>
import Profile from './Profile.vue';
import Gamestats from './Gamestats.vue';
export default {
	components: {
		Profile,
		Gamestats
	},
	data() {
		return {
			editProfile: false,
				}
	}
}

</script>