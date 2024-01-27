<template>
  <q-page>
    <episode-list :episode-api-params="{ is_favorited: true }" />
  </q-page>
</template>

<script setup lang="ts">
import EpisodeList from 'components/EpisodeList/EpisodeList.vue';
</script>
