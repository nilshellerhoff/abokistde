{% load static %}
Vue.component('searchfield', {
    delimiters : ['[[', ']]'],
    template : '#template-searchfield',
    data() {
        return {
            query: '',
            searchResults: [],
            isSearching: false,
            timer: null,
            searchDelay: 500,
        }
    },
    computed: {
        showResults: function() {
            if (this.query.trim() == '') {
                return false
            } else {
                return true
            }
        }
    },
    watch: {
        query: function() {
            this.searchTimeout()
        }
    },
    methods: {
        search: function() {
            if (this.query.trim() == '') {
                this.searchResults = []
            } else {
                this.isSearching = true;
                axios({
                    method: 'get',
                    url : "{% url 'home' %}search",
                    params: {
                        'query': this.query.trim()
                    }
                }).then((resp) => {
                    this.searchResults = resp.data.data
                    this.isSearching = false
                }).catch(() => {
                    this.isSearching = false
                })
            }
        },
        searchOnline: function() {
            if (this.query.trim() == '') {
                this.searchResults = []
            } else {
                this.isSearching = true;
                axios({
                    method: 'get',
                    url : "{% url 'home' %}search_online",
                    params: {
                        'query': this.query.trim()
                    }
                }).then((resp) => {
                    this.searchResults = resp.data.data
                    this.isSearching = false
                }).catch(() => {
                    this.isSearching = false
                })
            }
        },
        searchTimeout: function() {  
            if (this.timer) {
                clearTimeout(this.timer);
                this.timer = null;
            }
            this.timer = setTimeout(() => {
                this.search()
            }, this.searchDelay);
        },
        addChannel : async function(result) {
            await new Promise(r => setTimeout(r, 200));
            this.isSearching = true
            axios({
                method : 'post',
                url : '{% url "home" %}api/insert_channel',
                data : {
                    login_token : this.$parent.login_token,
                    channel_url : result.url,
                }
            }).then(() => {
                this.$root.fetchData();
                this.isSearching = false;
                this.query = '';
            }).catch(() => {
                this.isSearching = false;
            })
        }
    }
});

Vue.component('x-button', {
    template : `
        <img class="svg-filter" src="{% static 'assets/plus.svg' %}" style="transform: rotate(45deg); width: 100%; height: 100%;">
    `
});

Vue.component('plus-button', {
    template : `
    <img class="svg-filter" src="{% static 'assets/plus.svg' %}">
    ` 
});

// Add channel modal
Vue.component('add-channel', {
    template : '#template-add-channel',
    data() { 
        return {
            urlinput : '',
            submitting : false
        }
    },
    methods : {
        submit : async function() {
            this.submitting = true;
            await new Promise(r => setTimeout(r, 200));
            axios({
                method : 'post',
                url : '{% url 'home' %}api/insert_channel',
                data : {
                    login_token : this.$parent.login_token,
                    channel_url : this.$refs.url.value
                }
            }).then(() => {
                this.$root.fetchData();
                this.$root.modal = false;
            })
        }
    }
});

// User login component
Vue.component('user-login', {
    delimiters : ['[[', ']]'],
    template : '#template-user-login',
    data() {
        return {
            warningText : '&nbsp;',
            submitting : false
        }
    },
    methods : {
        userlogin : function() {
            this.submitting = true;
            axios({
                method : 'post',
                url : '{% url 'home' %}user/login',
                data : {
                    username : this.$refs.username.value,
                    password : this.$refs.password.value
                }
            }).then((response) => {
                // load login token into vue data
                this.$root.login_token = response.data.token;
                // set cookie with login data
                document.cookie = `login_token=${response.data.token}; SameSite=Strict`
                // load data
                this.$root.logged_in = true;
                this.$root.fetchData();
        }).catch(() => {
                this.warningText = 'Wrong password or username'
            }).finally(() => {
                this.submitting = false;
            });
        }
    }
});

// add user component
Vue.component('add-user', {
    delimiters : ['[[', ']]'],
    template : '#template-add-user',
    data() {
        return {
            warningText : '&nbsp;',
            submitting : false
        }
    },
    methods : {
        adduser : function() {
            username = this.$refs.username.value;
            password1 = this.$refs.password1.value;
            password2 = this.$refs.password2.value;

            // check if passwords match
            if (password1 != password2) {
                this.warningText = "Passwords do not match"
                return
            }

            this.submitting = true;
            
            axios({
                method : 'post',
                url : '{% url 'home' %}user/add',
                data : {
                    username : username,
                    password : password1
                }
            }).then(() => {
                // login with new user
                axios({
                    method : 'post',
                    url : '{% url 'home' %}user/login',
                    data : {
                        username : username,
                        password : password1
                    }
                }).then((response) => {
                    // load login token into vue data
                    this.$root.login_token = response.data.token;
                    // set cookie with login data
                    document.cookie = `login_token=${response.data.token}; SameSite=Strict`
                    // load data
                    this.$root.logged_in = true;
                    this.$root.fetchData();
                });
                this.$root.add_user = false;
            }).catch((error) => {
                console.log(error);
                this.warningText = error.response.data.message;
                return
            }).finally(() => {
                this.submitting = false;
            });
        }
    }
});

// video card component
Vue.component('video-card', {
    delimiters : ['[[', ']]'],
    template : '#template-video-card',
    props : [
        'channelThumbnail',
        'channelName',
        'providerThumbnail',
        'videoUrl',
        'videoTitle',
        'videoThumbnail',
        'videoRuntime',
        'videoUploadDate',
    ],
    computed : {
        runtimeString () {
            hours = Math.floor(this.videoRuntime / 3600)
            minutes = Math.floor((this.videoRuntime % 3600) / 60)
            seconds = Math.floor(this.videoRuntime % 60)

            hoursStr = hours.toString()
            minutesStr = hours > 0 ? minutes.toString().padStart(2, '0') : minutes.toString()
            secondsStr = seconds.toString().padStart(2, '0')

            if (hours > 0) return `${hoursStr}:${minutesStr}:${secondsStr}`
            else return `${minutesStr}:${secondsStr}`
        },
        uploadDateString () {
            years = Math.floor(this.videoUploadDate / 31536000)
            months = Math.floor((this.videoUploadDate % 31536000) / 2592000)
            days = Math.floor((this.videoUploadDate % 2592000) / 86400)
            hours = Math.floor((this.videoUploadDate % 86400) / 3600)
            minutes = Math.floor((this.videoUploadDate % 3600) / 60)
            seconds = Math.floor(this.videoUploadDate % 60)

            if (years > 1) return `${years} years ago`
            if (years == 1) return `${years} year ago`

            if (months > 1) return `${months} months ago`
            if (months == 1) return `${months} month ago`

            if (days > 1) return `${days} days ago`
            if (days == 1) return `${days} day ago`

            if (hours > 1) return `${hours} hours ago`
            if (hours == 1) return `${hours} hour ago`

            if (minutes > 1) return `${minutes} minutes ago`
            if (minutes == 1) return `${minutes} minute ago`

            if (seconds > 1) return `${seconds} seconds ago`
            else return `${seconds} second ago`
        }
    }
});

// Logo with text component 
Vue.component('logo-text', {
    template : '#template-logo-text'
});

var app = new Vue({
    el : "#app",
    delimiters : ['[[', ']]'],
    data : {
        loaded_data : '',
        videoFilter : '',
        modal : '',
        sidebar : false,
        updating : true,
        settings : false,
        login_token : '',
        logged_in : -1,
        add_user : false
    },
    created : function () {
        this.hideDisclaimer();
        this.readToken();
        this.checkToken();
    },
    methods : {
        hideDisclaimer : function() {
            // hide noscript prompt and render content
            window.vueloaded = "loaded";
            document.querySelector('#noscript').style.display='none';
            document.querySelector('#app').style.display='initial';
        },
        readToken : function() {
            // read login token from cookie
            try {
                this.login_token = document.cookie
                    .split('; ')
                    .find(row => row.startsWith('login_token'))
                    .split('=')[1];
            } catch (exception) {
                this.login_token = ""
            }
        },
        checkToken : function() {
            axios({
                method : 'post',
                url : '{% url 'home' %}user/check_token',
                data : {
                    login_token : this.login_token
                }
            }).then(() => {
                this.logged_in = true;
                this.fetchData();
            }).catch(() => {
                this.logged_in = false;
            });
        },
        fetchData : function() {
            this.updating = true;
            axios({
                method : 'post',
                url : '{% url 'home' %}api/videos',
                data : {
                    login_token : this.login_token
                }
            }).then((response) => {
                this.loaded_data = response.data;
                this.updating = false;
            });
        },
        updateBackend : function() {
            this.updating = true;
            axios({
                url : '{% url 'home' %}fetch_youtube'
            }).then(() => {
                this.fetchData();
            });
        },
        userlogout : function() {
            // delete local cookie and login_token
            axios({
                method : 'post',
                url : '{% url 'home' %}user/logout',
                data : {
                    login_token : this.login_token
                }
            }).then(() => {
                document.cookie = 'login_token=';
                document.cookie = 'sessionid='
                this.login_token = '';
                this.logged_in = false;
            });
        },
        deleteChannel : function(channel) {
            if (confirm(`Remove ${channel.name} from subscriptions?`)) {
                axios({
                    method : 'post',
                    url : '{% url 'home' %}api/delete_channel',
                    data : {
                        login_token : this.login_token,
                        channelid : channel.rowid
                    }
                }).then(() => {
                    this.sidebar = false;
                    this.fetchData();
                });
            }
        }
    }
});