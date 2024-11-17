<!--  -->
  <template>


<div class="container mt-5">
  <div class="row">
    <!-- First Row - Two Columns -->
    <div class="col-md-8  mb-3">
		  <div class="card">
			<div class="card-body">
			  <h1 class="card-title">My Friends</h1>
			  <!-- Search Input -->
			  <div class="d-flex align-items-center mb-3"> 
				<input
					v-model="searchQuery"
					@input="filterFriends"
					class="form-control mb-3"
					type="text"
					placeholder="Search for friends"
				/>
				<button type="button" class="btn" data-bs-toggle="modal" data-bs-target="#addFriendModal">
					<img id="add-friend" src="/assets/icons/person-add.svg" alt="Add Person" style="cursor: pointer;" @click="addPerson" />
			</button>

			</div> 
			  <!-- Friends List -->
				<div class="overflow-auto" style="max-height: 150px;">
					<ul v-if="filteredFriends.length" class="list-group">
						<li 
							id="friend"
							v-for="friend in filteredFriends"
							:key="friend.id"
							class="list-group-item"
							@click="selectFriend(friend)"
						>
							<div style="display: flex; align-items: center;">
								<!-- Profile Picture -->
								<img 
									:src="friend.profile_picture" 
									alt="Profile Picture" 
									class="rounded-circle" 
								/>
								
								<!-- Username -->
								<span style="margin-left: 10px; flex-grow: 1;">
									{{ friend.username }}
								</span>
								
								<!-- Online Status Dot -->
								<span 
									class="status-dot" 
									:class="{ 'status-online': friend.online, 'status-offline': !friend.online }"
									title="Online Status"
									style="width: 10px; height: 10px; border-radius: 50%; margin-right: 10px; display: inline-block;"
								></span>

								<!-- Decline Button -->
								<button 
									@click.stop="removeFriend(friend.id)" 
									class="btn btn-close" 
									title="Decline" 
									aria-label="Close" 
									style="padding: 0;"
								></button>
							</div>
						</li>

					</ul>
					<div v-else>
						<p>No friends found</p>
					</div>
				</div>
			</div>
	</div>
    </div>
    <div class="col-md-4 mb-3">
		<Profile
		class="p-3 border bg-light" 
		:editDisplay="editDisplay"
		/>
      <!-- <div class="p-3 border bg-light">Column 2</div> -->
    </div>
  </div>

		<div class="row mb-3">
			<!-- Second Row - One Column -->
			<div class="col-md-12">
				<div class="row">
					<div class="col-12">
						<div class="card">
							<div class="card-body">
								<h2 class="card-title">Friend Requests</h2>
								<p>This is a new section below the main content. You can add any content here, such as more forms, information, or controls.</p>
								<!-- You can add any content or components you need inside this new column -->
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
	<div class="modal fade" id="addFriendModal" tabindex="-1" aria-labelledby="addFriendModalLabel" aria-hidden="true" v-show="showModal">
		<div class="modal-dialog">
			<div class="modal-content">
			<div class="modal-header">
				<h5 class="modal-title" id="addFriendModalLabel">Add Friend</h5>
				<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="closeModal"></button>
			</div>
			<div class="modal-body">
				<!-- Add Friend Form -->
				<div class="mb-3">
				<label for="friendName" class="form-label">Friend's Name</label>
				<input 
					type="text" 
					class="form-control" 
					id="friendName" 
					v-model="newFriendName" 
					placeholder="Enter friend's name"
				/>
				</div>
			</div>
			<div class="modal-footer">
				<button type="button" class="btn btn-primary" @click="addFriend">Add Friend</button>
			</div>
			</div>
		</div>
		</div>
  </template>
  <script>
  import Profile from './Profile.vue';
  import axios from '../utils/axiosConfig';
  export default {
	name: 'Friends',
	data() {
	  return {
		editDisplay: false,
		searchQuery: '',
		showModal: true,
		newFriendName: '',
		friends: [
		  { id: 1, profile_picture: '/assets/images/default-profile.jpeg', username: 'John Doe', online: false },
		  { id: 2, profile_picture: '/assets/images/default-profile.jpeg', username: 'Jane Smith', online: false },
		  { id: 3, profile_picture: '/assets/images/default-profile.jpeg', username: 'Chris Johnson', online: true },
		  { id: 4, profile_picture: '/assets/images/default-profile.jpeg', username: 'Alex Brown', online: false },
		  { id: 5, profile_picture: '/assets/images/default-profile.jpeg', username: 'Emily White', online: true },
		],
		filteredFriends: [
		  { id: 1, profile_picture: '/assets/images/default-profile.jpeg', username: 'John Doe', online: false },
		  { id: 2, profile_picture: '/assets/images/default-profile.jpeg', username: 'Jane Smith', online: false },
		  { id: 3, profile_picture: '/assets/images/default-profile.jpeg', username: 'Chris Johnson', online: true },
		  { id: 4, profile_picture: '/assets/images/default-profile.jpeg', username: 'Alex Brown', online: false },
		  { id: 5, profile_picture: '/assets/images/default-profile.jpeg', username: 'Emily White', online: true },
		],
		friendsRequest: [
			{ id: 1, profile_picture: '/assets/images/default-profile.jpeg', username: 'John Doe', online: false },
			{ id: 2, profile_picture: '/assets/images/default-profile.jpeg', username: 'Jane Smith', online: false },
			{ id: 3, profile_picture: '/assets/images/default-profile.jpeg', username: 'Chris Johnson', online: true },
			{ id: 4, profile_picture: '/assets/images/default-profile.jpeg', username: 'Alex Brown', online: false },
			{ id: 5, profile_picture: '/assets/images/default-profile.jpeg', username: 'Emily White', online: true },
		],
	  };
	},
	components: {
	  Profile,
	},
	methods: {
	  filterFriends() {
		// Filter friends based on the search query
		this.filteredFriends = this.friends.filter((friend) =>
		  friend.username.toLowerCase().includes(this.searchQuery.toLowerCase())
		);
	  },
	  selectFriend(friend) {
		// Example function to handle selecting a friend (e.g., display more info)
		alert(`Selected friend: ${friend.username}`);
	  },
	  addPerson() {
		// Show the modal to add a new friend
		// Trigger the modal to add a new friend
		//   const modal = document.getElementById('addFriendModal');
		//   modal.show();
		//   this.showModal = true;
		},
		closeModal() {
			// Close the modal
			
			
			this.showModal = false;
		},
		addFriend() {
			// Handle adding the new friend to the list
			if (this.newFriendName) {
				const newFriend = { id: this.friends.length + 1, username: this.newFriendName };
				this.friends.push(newFriend);
				this.filteredFriends.push(newFriend);
				this.newFriendName = ''; // Reset the input field
				this.closeModal(); // Close the modal
			}
		},
		getFriends() {
			// Fetch friends from the server
			try {
				const response = axios.get(`https://${this.$router.ORIGIN_IP}:8000/api/user/get_friends`);
				console.log('Friends:', response.data.data);
				this.friends = response.data.data;
				this.filteredFriends = this.friends;
				switch (response.status) {
					case 200:
						console.log('Friends fetched successfully');
						break;
					default:
						console.error('Error fetching friends:', response.data);
						break;
				}
			} catch (error) {
				console.error('Error fetching friends:', error);
			}

		},
		getFriendsRequest() {
			// Fetch friends request from the server
			// Example: axios.get('/api/friends/request').then((response) => this.friendsRequest = response.data);
		},
	},
	mounted() {
		// this.getFriends();
		// this.getFriendsRequest();
  	},
}
  </script>
  
<style scoped>
#friend {
	/* width: 2.5rem */
	/* border-radius: 15px; */
	border-radius: 15px;
	margin-top: 5px; 
}

  #add-friend {
	display: flex;
	align-items: center;
	justify-content: center;
	/* margin-left: 2vh; */
	margin: 2vh;
	margin-bottom: 4vh;
	width: 2.5rem;
}
  /* Optional custom styling for the cards */
  .card {
	box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
	border-radius: 8px;
  }
  
  /* Adjust the spacing between cards */
  .mb-4 {
	margin-bottom: 1.5rem;
  }
  
  .card-title {
	font-size: 1.25rem;
	font-weight: bold;
  }
  
  .card-text {
	font-size: 1rem;
  }
  
  /* Optional styling for the search input */
  .form-control {
	width: 100%;
  }
  .status-dot {
    background-color: grey; /* Default offline color */
}

.status-online {
    background-color: green;
}

.status-offline {
    background-color: grey;
}
.rounded-circle {
	border : 2px solid rgba(255, 255, 255, 0.391);
	width: 40px; 
	height: 40px; 
  }

  .modal-content {
	background-color:  rgba(255, 255, 255, 0.638) !important;
	color: black;
  }
</style>
