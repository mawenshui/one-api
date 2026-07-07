import { useTheme } from '@mui/material/styles';
import { Box, Typography, Button, Container, Stack } from '@mui/material';
import Grid from '@mui/material/Unstable_Grid2';
import { GitHub } from '@mui/icons-material';

const BaseIndex = () => {
  const theme = useTheme();
  const isDark = theme.palette.mode === 'dark';

  // Hero background — uses theme palette (responsive to light/dark).
  // Light: bright indigo → purple (chat.mawenshui.work style).
  // Dark: deep dark with subtle indigo glow on the right.
  const heroBg = isDark
    ? `linear-gradient(135deg, #0b0d12 0%, #14171f 50%, #1d212c 100%)`
    : `linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)`;

  const textColor = isDark ? theme.palette.text.primary : '#ffffff';
  const subTextColor = isDark ? theme.palette.text.secondary : 'rgba(255, 255, 255, 0.92)';

  // GitHub button — keep brand black, but with theme-aware shadow.
  const btnShadow = isDark
    ? '0 4px 14px rgba(129, 140, 248, 0.4)'
    : '0 4px 14px rgba(99, 102, 241, 0.45)';

  return (
    <Box
      sx={{
        minHeight: 'calc(100vh - 136px)',
        background: heroBg,
        color: textColor,
        p: 4,
        transition: 'background 0.3s ease'
      }}
    >
      <Container maxWidth="lg">
        <Grid container columns={12} wrap="nowrap" alignItems="center" sx={{ minHeight: 'calc(100vh - 230px)' }}>
          <Grid md={7} lg={6}>
            <Stack spacing={3}>
              <Typography variant="h1" sx={{ fontSize: '4rem', color: textColor, lineHeight: 1.5 }}>
                MWS の One Api
              </Typography>
              <Typography
                variant="h4"
                sx={{ fontSize: '1.5rem', color: subTextColor, lineHeight: 1.5 }}
              >
                统一 LLM API 网关 <br />
                整合 29 个 AI 渠道 · 一份 Key 走天下 <br />
                自托管 · 开箱即用
              </Typography>
              <Button
                variant="contained"
                startIcon={<GitHub />}
                href="https://github.com/mawenshui/one-chat"
                target="_blank"
                sx={{
                  backgroundColor: '#24292e',
                  color: '#fff',
                  width: 'fit-content',
                  boxShadow: btnShadow,
                  '&:hover': { backgroundColor: '#1b1f23' }
                }}
              >
                GitHub
              </Button>
            </Stack>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
};

export default BaseIndex;
