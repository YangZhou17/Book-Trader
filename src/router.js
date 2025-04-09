import {createRouter, createWebHashHistory} from "vue-router"
const routes = [
    {
        path: '/',
        redirect: '/login',
        children:[
            {
                path: '/login',
                component: () => import('./components/pages/UserLogin.vue'),
                mata: {title: 'User Login'}, 
                name: 'User Login',
            },
            {
                path: '/register',
                component: () => import('./components/pages/UserRegister.vue'),
                mata: {title: 'User Register'}, 
                name: 'User Register',
            },
            {
                path: '/main',
                component: () => import('./components/pages/Main.vue'),
                mata: {title: 'Shelf Overview'},
                name: 'Shelf Overview',
            },
            {
                path: '/profile/:username',
                component: () => import('./components/pages/UserProfile.vue'),
                mata: {title: 'User Profile'},
                name: 'User Profile',
                props: true,
            },
            {
                path: '/followers',
                component: () => import('./components/pages/UserFollowers.vue'),
                mata: {title: 'User Follower'},
                name: 'User Follower',
            },
            {
                path: '/following',
                component: () => import('./components/pages/UserFollowing.vue'),
                mata: {title: 'User Followings'},
                name: 'User Followings',
            },
            // {
            //     path: '/import',
            //     component: () => import('./components/pages/Import.vue'),
            //     mata: {title: 'Import'},
            //     name: 'Import',
            // },
            
            {
                path: '/upload',
                component: () => import('./components/pages/UploadBook.vue'),
                mata: {title: 'Create Shelf'},
                name: 'Create Shelf',
            },
            // {
            //     path: '/index/manage/blank',
            //     component: () => import('./components/pages/BlankPage.vue'),
            //     name: 'blank',
            //     meta: {title:'blank'}
            // },
        ]
    }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

export default router


