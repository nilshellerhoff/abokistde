<template id="templateEpisodeCard">
  <v-card class="mx-auto"
          max-width="344"
          :href="episode.url"
          target="_blank"
  >
    <div class="pa-2 text-truncate">
      <v-avatar :image="episode.publishing_channel.thumbnail_url"
                size="20"></v-avatar>
      [[ episode.publishing_channel.name ]]
    </div>
    <v-img
        :src="episode.thumbnail_url"
        aspect-ratio="1.7778"
        cover>

      <div class="position-absolute"
           style="top: 4px; right: 4px">
        <v-btn icon
               color="#ffffffbb"
               size="36"
               @click.prevent="hideUnhideEpisode(episode)"
        >
          <v-icon v-if="episode.is_hidden">mdi-eye</v-icon>
          <v-icon v-else>mdi-eye-off</v-icon>
          <v-tooltip
              activator="parent"
          >[[ episode.is_hidden ? "unhide episode" : "hide episode" ]]
          </v-tooltip>
        </v-btn>
      </div>
    </v-img>
    <v-card-title style="font-size: 1em">
      [[ episode.title ]]
    </v-card-title>

    <v-tooltip
        activator="parent"
        location="bottom"
    >[[ episode.title ]]
    </v-tooltip>
  </v-card>
</template>

<script>
const episodeCard = {
  template: '#templateEpisodeCard',
  delimiters: ['[[', ']]'],
  props: ['episode'],
  methods: {
    hideUnhideEpisode(episode) {
      this.$emit('hide-unhide-episode', episode);
    }
  }
}
app.component('episodeCard', episodeCard);
</script>