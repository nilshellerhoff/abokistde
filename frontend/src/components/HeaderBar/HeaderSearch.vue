<template>
  <q-toolbar-title v-if="!isSearching || !hideLogoIfSearching">
    <div class="q-pa-sm">
      <AbokistdeLogo :height="50" />
    </div>
  </q-toolbar-title>
  <q-input
    v-model="searchQuery"
    v-if="isSearching"
    style="width: 100%; max-width: 600px"
    class="mx-auto"
    placeholder="Search..."
    autofocus
    dark
    @keyup.enter="$router.push(`/search/${searchQuery}`)"
    
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

  <q-space v-if="isSearching" />
  <q-btn
    flat
    :icon="isSearching ? 'close' : 'search'"
    @click="
      isSearching = !isSearching;
      searchQuery = '';
      $router.push(isSearching ? '/search' : '/');
    "
  ></q-btn>
</template>

<script setup lang="ts">
import AbokistdeLogo from 'components/AbokistdeLogo.vue';
import { useRoute } from 'vue-router';
import { computed, ref } from 'vue';

const route = useRoute();

const isSearching = ref(false);
const searchQuery = ref('');

const hideLogoIfSearching = computed(() => window.innerWidth < 1240);

if (route.name == 'search') {
  const query = route.params.query;
  searchQuery.value = typeof query === 'string' ? query : query[0];
  isSearching.value = true;
}
</script>
