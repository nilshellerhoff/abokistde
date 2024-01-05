<template>
  <q-page>
    <episode-list :episode-api-params="{ is_subscribed: true }" />
  </q-page>
</template>

<script setup lang="ts">
import EpisodeList from 'components/EpisodeList.vue';
</script>
