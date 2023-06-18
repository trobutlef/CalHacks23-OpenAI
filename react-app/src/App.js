import React from "react";
import VideoUpload from "./VideoUpload";
import VideoPlayer from "./VideoPlayer";
import GetTimeStamps from "./GetTimeStamps";
import {
  Box,
  Container,
  Grid,
  Typography,
  createTheme,
  ThemeProvider,
} from "@mui/material";

const theme = createTheme({
  palette: {
    background: {
      default: "#f0f0f0", // You can set your desired color here.
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <Container maxWidth="lg">
        <Typography variant="h2" align="center" gutterBottom>
          Video Analysis to Text with OpenAI
        </Typography>
        <Box my={4}>
          <Grid container spacing={4} direction="column" alignItems="center">
            <Grid item xs={12} sm={8}>
              <VideoUpload />
            </Grid>
            <Grid item xs={12} sm={8}>
              <GetTimeStamps />
            </Grid>
          </Grid>
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App;
