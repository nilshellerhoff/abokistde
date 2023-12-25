<template id="templateEpisodeOverview">
  <div v-if="!isLoading && (!channels || channels.length == 0)"
       class="text-center">
    <span class="text-h5">You don't have any channels yet.</span><br>
    <span class="text-subtitle-1">Add your first in the sidebar to the left!</span>
  </div>
  <div v-else-if="!isLoading && (!episodes || episodes.length == 0)">
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
  <div v-if="!isLoading"
       class="text-center ma-16">
    <v-btn @click="fetchEpisodes">Load more</v-btn>
  </div>
  <div v-if="isLoading"
       class="text-center">
    <loading-indicator class="mx-auto my-16"
                       style="width: 40px"></loading-indicator>
  </div>
</template>

<script>
const episodeOverview = {
  template: '#templateEpisodeOverview',
  delimiters: ['[[', ']]'],
  inject: ["channelFilter", "updateEpisodesCounter", "updateChannelsCounter"],
  data() {
    return {
      isLoading: 0,
      currentOffset: 0,
      pageSize: 48,
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
        this.channels = response.data.results
      }).finally(() => {
        this.isLoading--;
      })
    },
    fetchEpisodes() {
      this.isLoading++;

      let query_params = {
        offset: this.currentOffset,
        limit: this.pageSize,
      }

      if (this.channelFilter) {
        query_params.publishing_channel = this.channelFilter.id
      }

      axios({
        method: 'get',
        url: "/api/episode_user/",
        params: query_params,
      }).then((response) => {
        this.episodes = [...this.episodes, ...response.data.results]
        this.currentOffset += this.pageSize
      }).finally(() => {
        this.isLoading--;
      })
    },
    resetEpisodes() {
      this.episodes = []
      this.currentOffset = 0
    },
    resetChannels() {
      this.channels = []
    }
  },
  mounted() {
    this.fetchChannels()
    this.fetchEpisodes()
  },
  watch: {
    channelFilter: function () {
      this.resetEpisodes()
      this.fetchEpisodes()
    },
    updateChannelsCounter: function () {
      this.resetChannels()
      this.fetchChannels()
    },
    updateEpisodesCounter: function () {
      this.resetEpisodes()
      this.fetchEpisodes()
    },
  }
}
app.component("episodeOverview", episodeOverview)
</script>