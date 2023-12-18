<template id="templateEpisodeOverview">
  <v-row dense>
    <v-col v-for="episode in episodes"
           :key="episode.id"
           :cols="12 / amountOfCols"
           :style="!channelFilter || episode.publishing_channel__id == channelFilter.id ? 'display: block' : 'display: none'"
    >
      <episode-card :episode="episode"></episode-card>
    </v-col>
  </v-row>

</template>

<script>
const episodeOverview = {
  template: '#templateEpisodeOverview',
  delimiters: ['[[', ']]'],
  inject: ["channelFilter"],
  data() {
    return {
      episodes: window.episodes,
    }
  },
  computed: {
    amountOfCols() {
      if (window.innerWidth > 1200) return 4
      if (window.innerWidth > 1000) return 3
      if (window.innerWidth > 600) return 2
      return 1
    }
  }
}
app.component("episodeOverview", episodeOverview)
</script>