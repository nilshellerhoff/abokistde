<template id="templateEpisodeOverview">
  <div v-if="isLoading"
       class="text-center">
    <v-progress-circular indeterminate></v-progress-circular>
  </div>
  <div v-else>
    <div v-if="!channels || channels.length == 0"
         class="text-center">
      <span class="text-h5">You don't have any channels yet.</span><br>
      <span class="text-subtitle-1">Add your first in the sidebar to the left!</span>
    </div>
    <div v-else-if="!episodes || episodes.length == 0">
      <span class="text-h5">No episodes found.</span>
    </div>
    <div v-else>
      <v-row dense>
        <v-col v-for="episode in episodes"
               :key="episode.id"
               :cols="12 / amountOfCols"
               :style="!channelFilter || episode.publishing_channel.id == channelFilter.id ? 'display: block' : 'display: none'"
        >
          <episode-card :episode="episode"></episode-card>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script>
const episodeOverview = {
  template: '#templateEpisodeOverview',
  delimiters: ['[[', ']]'],
  inject: ["channelFilter"],
  data() {
    return {
      isLoading: 0,
      episodes: [],
      channels: [],
    }
  },
  computed: {
    amountOfCols() {
      if (window.innerWidth > 1200) return 4
      if (window.innerWidth > 1000) return 3
      if (window.innerWidth > 600) return 2
      return 1
    }
  },
  methods: {
    fetchChannels() {
      this.isLoading++;
      axios({
        method: 'get',
        url: "/api/publishing_channel_user",
      }).then((response) => {
        this.channels = response.data
      }).finally(() => {
        this.isLoading--;
      })
    },
    fetchEpisodes() {
      this.isLoading++;
      axios({
        method: 'get',
        url: "/api/episode_user",
      }).then((response) => {
        this.episodes = response.data
      }).finally(() => {
        this.isLoading--;
      })
    },
  },
  mounted() {
    this.fetchChannels()
    this.fetchEpisodes()
  }
}
app.component("episodeOverview", episodeOverview)
</script>