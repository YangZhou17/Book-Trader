import {createRouter, createWebHashHistory} from "vue-router"
const routes = [
    {
        path: '/',
        redirect: '/index/manage/dataset',
        children:[
            {
                path: '/index/manage/dataset',
                component: () => import('./components/pages/Main.vue'),
                mata: {title: 'Shelf Overview'},
                name: 'Shelf Overview',
            },
            {
                path: '/index/manage/dataset/insert',
                component: () => import('./components/pages/Import.vue'),
                mata: {title: 'Import'},
                name: 'Import',
            },
            
            {
                path: '/index/manage/dataset/create',
                component: () => import('./components/pages/CreateSet.vue'),
                mata: {title: 'Create Shelf'},
                name: 'Create Shelf',
            },
            {
                path: '/index/manage/blank',
                component: () => import('./components/pages/BlankPage.vue'),
                name: 'blank',
                meta: {title:'blank'}
            },
            
            
            
        ]
    }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

export default router


