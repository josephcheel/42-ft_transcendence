<template>
	<div class="container">
	  <div class="row justify-content-between">
		<!-- Card 1 - Friends Section -->
		<div class="col-12 col-md-8 mb-4">
		  <div class="card">
			<div class="card-body">
			  <h1 class="card-title">{{ $t('friends.friends_title')}}</h1>
			  <!-- Search Input -->
			  <div class="d-flex align-items-center mb-3"> 
				<input
					v-model="searchQuery"
					@input="filterFriends"
					class="form-control mb-3"
					type="text"
					:placeholder="$t('friends.placeholder_search')"
				/>
				<button type="button" class="btn" data-bs-toggle="modal" data-bs-target="#addFriendModal">
					<img id="add-friend" src="/assets/icons/person-add.svg" alt="Add Person" style="cursor: pointer;" @click="addPerson" />
			</button>

			</div> 
			  <!-- Friends List -->
			  <div class="overflow-auto" style="max-height: 150px;">
			  <ul class="list-group">
				<li 
				  id="friend"
				  v-for="friend in filteredFriends"
				  :key="friend.id"
				  class="list-group-item"
				  @click="selectFriend(friend)"
				>
				  {{ friend.name }}
				</li>
			  </ul>
			  </div>
			</div>
		  </div>
		</div>
  
		<!-- Card 2 -->
		<div class="col-12 col-md-4">
			  <Profile :editDisplay="editDisplay"/>
		</div>


		<div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-body">
            <h2 class="card-title">{{ $t('friends.requests_title')}}</h2>
            <p>This is a new section below the main content. You can add any content here, such as more forms, information, or controls.</p>
            <!-- You can add any content or components you need inside this new column -->
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
			<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <!-- <button type="button" class="btn btn-secondary" @click="closeModal">Close</button> -->
            <button type="button" class="btn btn-primary" @click="addFriend">Add Friend</button>
          </div>
        </div>
      </div>
    </div>


	  </div>
	</div>
  </template>
  
  <script>
  import Profile from './Profile.vue';
  
  export default {
	name: 'MainComponent',
	data() {
	  return {
		editDisplay: false,
		searchQuery: '',
		showModal: true,
		newFriendName: '',
		friends: [
		  { id: 1, name: 'John Doe' },
		  { id: 2, name: 'Jane Smith' },
		  { id: 3, name: 'Chris Johnson' },
		  { id: 4, name: 'Alex Brown' },
		  { id: 5, name: 'Emily White' },
		],
		filteredFriends: [
		  { id: 1, name: 'John Doe' },
		  { id: 2, name: 'Jane Smith' },
		  { id: 3, name: 'Chris Johnson' },
		  { id: 4, name: 'Alex Brown' },
		  { id: 5, name: 'Emily White' },
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
		  friend.name.toLowerCase().includes(this.searchQuery.toLowerCase())
		);
	  },
	  selectFriend(friend) {
		// Example function to handle selecting a friend (e.g., display more info)
		alert(`Selected friend: ${friend.name}`);
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
        const newFriend = { id: this.friends.length + 1, name: this.newFriendName };
        this.friends.push(newFriend);
        this.filteredFriends.push(newFriend);
        this.newFriendName = ''; // Reset the input field
        this.closeModal(); // Close the modal
      }
    },
	},
  };
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
</style>
