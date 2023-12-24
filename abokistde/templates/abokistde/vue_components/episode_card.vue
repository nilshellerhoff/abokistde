<template id="templateEpisodeCard">
  <v-card class="mx-auto"
          max-width="344"
          :href="episode.url"
          target="_blank"
  >
    <div class="pa-2 text-truncate">
      <v-avatar :image="episode.publishing_channel.thumbnail_url" size="20"></v-avatar>
      [[ episode.publishing_channel.name ]]
    </div>
    <v-img
        :src="episode.thumbnail_url"
        aspect-ratio="1.7778"
        cover></v-img>
    <v-card-title style="font-size: 1em">
      [[ episode.title ]]
    </v-card-title>

    <v-tooltip
        activator="parent"
        location="bottom"
    >[[ episode.title ]]</v-tooltip>
  </v-card>
</template>

<script>
const episodeCard = {
  template: '#templateEpisodeCard',
  delimiters: ['[[', ']]'],
  props: ['episode'],
}

app.component('episodeCard', episodeCard);
</script>