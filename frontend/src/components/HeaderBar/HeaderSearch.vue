<template>
  <q-toolbar-title v-if="!isSearching">
    <div class="q-pa-sm">
      <AbokistdeLogo :height="50" />
    </div>
  </q-toolbar-title>
  <q-input
    v-model="searchQuery"
    v-if="isSearching"
    style="width: 100%; background-color: #fff"
    class=""
    placeholder="Search..."
    autofocus
  >
    <template #prepend>
      <q-icon name="search" />
    </template>

    <template #append>
      <q-btn
        flat
        round
        dense
        icon="arrow_forward"
        :to="`/search/${searchQuery}`"
        :disable="searchQuery.trim() === ''"
      />
    </template>
  </q-input>

  <q-btn
    flat
    :icon="isSearching ? 'close' : 'search'"
    @click="isSearching = !isSearching"
  ></q-btn>
</template>

<script setup lang="ts">
import AbokistdeLogo from 'components/AbokistdeLogo.vue';
import { useRoute } from 'vue-router';
import { ref } from 'vue';

const route = useRoute();

const isSearching = ref(false);
const searchQuery = ref('');

if (route.name == 'search') {
  const query = route.params.query;
  searchQuery.value = typeof query === 'string' ? query : query[0];
  isSearching.value = true;
}
</script>
