<template>
  <search-results :search-value="$route.params.query" />
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router';
import SearchResults from 'components/SearchResults.vue';

const route = useRoute();

console.log(route.params.query);

const query = route.params.query;
</script>
