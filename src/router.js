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
            {
                path: '/transactions',
                component: () => import('./components/pages/UserTransactions.vue'),
                mata: {title: 'User Transactions'},
                name: 'User Transactions',
            },  
            {
                path: '/upload',
                component: () => import('./components/pages/UploadBook.vue'),
                mata: {title: 'Create Shelf'},
                name: 'Create Shelf',
            },
            {
                path: '/transactionConfirm',
                component: () => import('./components/pages/TransactionConfirmation.vue'),
                mata: {title: 'Confirm Transaction'},
                name: 'Confirm Transaction',
                props: true,
            },
        ]
    }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

export default router


