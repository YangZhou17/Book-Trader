<!-- Bookshelf Display Page -->
<template>
    <el-container>
      <!-- Header Element -->
      <el-header>
        <Breadcrumb />
      </el-header>
      <el-divider />
  
      <!-- Main Section -->
      <el-main>
        <!-- Page title -->
        <el-row>
          <h1>{{ pageTitle }}</h1>
        </el-row>
        <br />
  
        <!-- Search bar -->
        <el-row v-if="pageType === 'recommend'" :gutter="12" align="middle">
          <el-col :span="4">
            <el-input
              v-model="searchQuery"
              placeholder="Search books by name"
              clearable
              prefix-icon="el-icon-search"
              @keyup.enter="searchBooks"
            />
          </el-col>
          <el-col :span="4">
            <el-select v-model="transactionType" placeholder="Transaction Type" clearable>
              <el-option label="Sell" value="sell" />
              <el-option label="Rent" value="rent" />
            </el-select>
          </el-col>
          <el-col :span="4">
            <el-input
              v-model="usernameFilter"
              placeholder="Owner username"
              clearable
              @keyup.enter="searchBooks"
            />
          </el-col>
          <el-col :span="3">
            <el-input-number
              v-model="minPrice"
              :min="0"
              placeholder="Min Price"
              style="width: 100%"
              @keyup.enter="searchBooks"
            />
          </el-col>
          <el-col :span="3">
            <el-input-number
              v-model="maxPrice"
              :min="0"
              placeholder="Max Price"
              style="width: 100%"
              @keyup.enter="searchBooks"
            />
          </el-col>
          <el-col :span="4">
            <el-input-number
              v-model="rentDuration"
              :min="0"
              placeholder="Rent Duration (days)"
              style="width: 100%"
              @keyup.enter="searchBooks"
            />
          </el-col>
          <el-col :span="2">
            <el-button type="primary" @click="searchBooks">Search</el-button>
          </el-col>
        </el-row>
        <br />
  
        <!-- displaying books -->
        <el-empty v-if="fetchedBooks.length === 0" description="No books found" />
        <el-table
          v-else
          :data="fetchedBooks"
          height="400"
          style="width: 100%"
          border
        >
          <el-table-column prop="name" label="Name" />
          <el-table-column
            prop="transaction_type"
            label="Transaction Type"
            width="120"
            align="center"
          />
          <el-table-column
            prop="price"
            label="Price"
            width="100"
            align="center"
          />
          <el-table-column prop="owner" label="Owner" width="140" align="center">
            <template v-slot="{ row }">
              <el-link
                :underline="false"
                @click="goToUploaderProfile(row.owner)"
              >
                {{ row.owner }}
              </el-link>
            </template>
          </el-table-column>
          <el-table-column
            prop="uploaded_at"
            label="Uploaded At"
            width="140"
            align="center"
          >
            <template v-slot="{ row }">
              {{ formatDate(row.uploaded_at) }}
            </template>
          </el-table-column>
          <el-table-column
            label="Rent Duration (days)"
            width="160"
            align="center"
          >
            <template v-slot="{ row }">
              {{ row.rent_duration || '(n/a)' }}
            </template>
          </el-table-column>
          <el-table-column label="Action" width="150" align="center">
            <template v-slot="{ row }">
              <div v-if="row.owner !== currentUser">
                <el-button
                  v-if="row.transaction_type === 'sell'"
                  type="success"
                  @click="buyBook(row)"
                >
                  Buy
                </el-button>
                <el-button
                  v-else-if="row.transaction_type === 'rent'"
                  type="success"
                  @click="rentBook(row)"
                >
                  Rent
                </el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </el-main>
    </el-container>
  </template>
  
  <script>
  import Breadcrumb from "../BreadCrumb.vue";
  
  export default {
    name: "MainPage",
    components: { Breadcrumb },
    data() {
      return {
        currentUser: localStorage.getItem("username") || "",
        pageType: "",
        pageTitle: "",
        fetchedBooks: [],
        searchQuery: "",
        transactionType: "",
        usernameFilter: "",
        minPrice: null,
        maxPrice: null,
        rentDuration: null,
      };
    },
  
    watch: {
      '$route.query.pageType': {
        immediate: true,
        handler(newVal) {
          this.loadPage(newVal);
        },
      },
    },
  
    methods: {
      loadPage(type) {
        console.log("Loading main page of type: " + type);
        this.pageType = this.$route.query.pageType;
        this.renderPageTitle();
        this.fetchBooks();
      },
  
      fetchBooks() {
        const url = `http://localhost:5001/api/books/${this.pageType}/${this.currentUser}`;
        fetch(url, {
          method: "GET",
          headers: { "content-type": "application/json" },
        })
          .then((r) => r.json())
          .then((data) => {
            if (data.success) {
              this.fetchedBooks = data.books;
            }
          })
          .catch(console.error);
      },
  
      searchBooks() {
        const noParams =
          !this.searchQuery.trim() &&
          !this.transactionType &&
          !this.usernameFilter.trim() &&
          this.minPrice == null &&
          this.maxPrice == null &&
          this.rentDuration == null;

        if (noParams) {
          return this.fetchBooks();
        }
                
        const params = new URLSearchParams();
        if (this.searchQuery.trim()) {
          params.append("book_name", this.searchQuery.trim());
        }
        if (this.transactionType) {
          params.append("transaction_type", this.transactionType);
        }
        if (this.usernameFilter.trim()) {
          params.append("username", this.usernameFilter.trim());
        }
        if (this.minPrice !== null) {
          params.append("min_price", this.minPrice);
        }
        if (this.maxPrice !== null) {
          params.append("max_price", this.maxPrice);
        }
        if (this.rentDuration !== null) {
          params.append("rent_duration", this.rentDuration);
        }
  
        const url = `http://localhost:5001/api/books/search?${params.toString()}`;
        fetch(url, {
          method: "GET",
          headers: { "content-type": "application/json" },
        })
          .then((r) => r.json())
          .then((data) => {
            if (data.success) {
              this.fetchedBooks = data.books;
            } else {
              this.$message.warning(data.message || "Search failed");
            }
          })
          .catch((err) => {
            console.error(err);
            this.$message.error("Error while searching");
          });
      },
  
      formatDate(datetime) {
        return datetime ? datetime.split("T")[0] : "";
      },
  
      renderPageTitle() {
        switch (this.pageType) {
          case "nearby":
            this.pageTitle = "Books From Your School";
            break;
          case "following":
            this.pageTitle = "Books From People You Are Following";
            break;
          default:
            this.pageTitle = "Books Recommended For You";
        }
      },
  
      toUpload() {
        this.$router.push("/upload");
      },
  
      goToUploaderProfile(username) {
        this.$router.push(`/profile/${username}`);
      },
  
      buyBook(book) {
        this.$router.push({
          path: "/transactionConfirm",
          query: {
            book_id: book.id,
            book_name: book.name,
            book_price: book.price,
            book_owner: book.owner,
            book_uploaded: book.uploaded_at,
            transaction_type: "buy",
          },
        });
      },
  
      rentBook(book) {
        this.$router.push({
          path: "/transactionConfirm",
          query: {
            book_id: book.id,
            book_name: book.name,
            book_price: book.price,
            book_owner: book.owner,
            book_uploaded: book.uploaded_at,
            book_rent_duration: book.rent_duration,
            transaction_type: "rent",
          },
        });
      },
    },
  };
  </script>
  
  <style scoped>
  .el-header {
    height: 56px;
  }
  .el-divider {
    margin: 0;
  }
  </style>
  