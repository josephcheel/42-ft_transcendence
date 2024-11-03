<template>

<div>
    Hello from Gamestats
</div>    
    
</template>
<script>
    import axios from 'axios';

    export default {
    name: 'Gamestats',
    data() {
        return {
            matchList: []
        }
    },
    methods:
    {
        getMatchList()
        {
            axios.get(`https://${this.$router.ORIGIN_IP}:8000/api/tournaments/list_matches/`)
            .then(response => {
                this.matchList = response.data.data;
                console.log(this.matchList);

            })
            .catch(error => {
                console.error("Error fetching match list:", error);
            });
        }
    },
    mounted() {
        this.getMatchList();
    }
}
</script>
    
<script setup>
</script>

    
<style scoped>

</style>