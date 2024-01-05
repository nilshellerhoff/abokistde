<template id="templateChannelList">
  <v-navigation-drawer
      v-model="drawer"
      :width="400"
  >
    <template #prepend>
      <v-text-field
          variant="outlined"
          prepend-inner-icon="mdi-magnify"
          v-model="searchValue"
          @update:model-value="searchDebounced"
          placeholder="Search channels"
          class="px-2 pt-4"
      ></v-text-field>
    </template>
    <div v-if="isLoading"
         class="text-center">
      <loading-indicator class="mx-auto" style="width: 40px"></loading-indicator>
    </div>
    <v-list>
      <v-list-item
          v-for="subscription in subscriptionsFiltered"
          :key="subscription.id"
          :value="subscription"
          color="primary"
          class="pa-2"
          @click="setChannelFilter(subscription.publishing_channel)"
      >
        <template v-slot:prepend>
          <v-avatar :image="subscription.publishing_channel.thumbnail_url"
                    icon="mdi-account-outline"></v-avatar>
        </template>
        <v-list-item-title v-text="subscription.publishing_channel.name"></v-list-item-title>
        <template v-slot:append>
          <remove-channel-button
              :subscription="subscription"
          ></remove-channel-button>
        </template>

      </v-list-item>
      <v-divider></v-divider>
      <span v-if="searchValue">
      <v-list-subheader>Search results</v-list-subheader>
      <v-list-item v-if="isSearching"
                   class="text-center">
        <loading-indicator class="mx-auto" style="width: 40px"></loading-indicator>
      </v-list-item>
      <v-list-item
          v-else
          class="text-center">
      <v-btn @click="searchOnline">
        Search on Youtube
      </v-btn>
        </v-list-item>
      <v-list-item
          v-for="channel in searchResults"
          :key="channel.id"
          :value="channel"
          color="primary"
          class="pa-2"
      >
        <template v-slot:prepend>
          <v-avatar :image="channel.thumbnail_url"
                    icon="mdi-account-outline"></v-avatar>
        </template>
        <v-list-item-title v-text="channel.name"></v-list-item-title>
        <template v-slot:append>
          <add-channel-button
              :channel="channel"
              :disabled="subscriptions.find(s => s.publishing_channel.id === channel.id)"
          ></add-channel-button>
        </template>
      </v-list-item>
    </span>
    </v-list>
    <template v-slot:append>
      <github-link></github-link>
    </template>
  </v-navigation-drawer>
</template>

<script>
const channelList = {
  template: "#templateChannelList",
  delimiters: ['[[', ']]'],
  inject: ["channelFilter", "drawer", "updateChannelsCounter"],
  data() {
    return {
      channels: [],
      subscriptions: [],
      isLoading: 0,
      searchResults: [],
      searchValue: "",
      isSearching: false,
    }
  },
  computed: {
    subscriptionsFiltered() {
      return this.subscriptions.filter(s => s.publishing_channel.name.toLowerCase().includes(this.searchValue.toLowerCase()))
    }
  },
  methods: {
    fetchSubscriptions() {
      this.isLoading++;
      axios({
        method: 'get',
        url: "/api/user_subscription/",
      }).then((response) => {
        this.subscriptions = response.data.results
        this.channels = response.data.results.map(s => s.publishing_channel)
      }).finally(() => {
        this.isLoading--;
      })
    },
    search() {
      this.searchResults = []
      if (this.searchValue.trim() !== '') {
        this.isSearching = true;
        axios({
          method: 'get',
          url: "/api/publishing_channel",
          params: {
            'search': this.searchValue.trim()
          }
        }).then((response) => {
          this.searchResults = response.data.results
        }).finally(() => {
          this.isSearching = false
        })
      }
    },
    searchDebounced: _.debounce(function () {
      this.search()
    }, 500),
    searchOnline: function () {
      this.searchResults = []
      if (this.searchValue.trim() !== '') {
        this.isSearching = true;
        axios({
          method: 'get',
          url: "/search_online",
          params: {
            'query': this.searchValue.trim()
          }
        }).then((response) => {
          this.searchResults = response.data.data
          this.isSearching = false
        }).catch(() => {
          this.isSearching = false
        })
      }
    },
    setChannelFilter(channel) {
      this.channelFilter = channel;
    }
  },
  mounted() {
    this.fetchSubscriptions()
  },
  watch: {
    updateChannelsCounter: function () {
      this.fetchSubscriptions()
    }
  }
}

app.component("channelList", channelList)
app.provide("channelFilter", Vue.ref(null))
app.provide("drawer", Vue.ref(null))
app.provide("updateEpisodesCounter", Vue.ref(0))
app.provide("updateChannelsCounter", Vue.ref(0))
</script>